from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Union

from .ProjectInstance import (
    Activity,
    Mode,
    Project,
    ProjectInstance,
    Resource,
)


@dataclass
class AlternativeSubgraph:
    """
    Represents a single alternative subgraph in an ASLIB instance.

    Parameters
    ----------
    branches
        A list of branches in the subgraph. Each branch is a list of activity
        indices that are part of the branch.
    """

    branches: list[list[int]]


def _parse_part_a(lines):
    """
    Part (a) of ASLIB instance is formatted as Patterson instance.
    """
    num_activities, num_resources = map(int, next(lines).split())

    # Instances without resources do not have an availability line.
    capacities = list(map(int, next(lines).split())) if num_resources else []
    resources = [Resource(capacity=cap, renewable=True) for cap in capacities]

    activities = []
    for _ in range(num_activities):
        values = map(int, next(lines).split())
        duration = int(next(values))
        demands = [int(next(values)) for _ in range(num_resources)]
        num_successors = int(next(values))
        successors = [int(next(values)) - 1 for _ in range(num_successors)]
        activities.append(Activity([Mode(duration, demands)], successors))

    return resources, activities


def _parse_part_b(lines) -> list[AlternativeSubgraph]:
    """
    Part (b) of ASLIB instance results in alternative subgraphs.
    """
    pct_flex, pct_nested, pct_linked = map(float, next(lines).split())
    num_subgraphs = int(next(lines))
    total_branches = 1  # first branch is always the dummy branch
    subgraphs = []

    for _ in range(num_subgraphs):
        num_branches, *branch_idcs = map(int, next(lines).split())
        total_branches += num_branches
        branch_idcs = [idx - 1 for idx in branch_idcs]
        subgraphs.append(branch_idcs)

    branches: list[list[int]] = [[] for _ in range(total_branches)]
    for activity, line in enumerate(lines):
        num_braches, *branch_idcs = map(int, line.split())
        for idx in branch_idcs:
            branches[idx - 1].append(activity)

    # Return the alternative subgraphs, with the first subgraph containing the
    # fixed activities (an activity belongs to node branch 0 if it is fixed).
    result = [AlternativeSubgraph([branches[0]])]
    result += [
        AlternativeSubgraph([branches[idx] for idx in branch_idcs])
        for branch_idcs in subgraphs
    ]

    return result


def parse_aslib(loc: Union[str, Path]) -> ProjectInstance:
    """
    Parses an ASLIB-formatted instance from a file. This format is used for
    RCPSP instances with alternative subgraphs.

    Note
    ----
    This function parses files that combine both "a" and "b" part files from
    the ASLIB instance. You have to manually create such instances first!

    Parameters
    ----------
    loc
        The location of the instance.

    Returns
    -------
    ProjectInstance
        The parsed project instance.
    """
    with open(loc, "r") as fh:
        lines = iter(line.strip() for line in fh.readlines() if line.strip())

    resources, activities = _parse_part_a(lines)
    subgraphs = _parse_part_b(lines)

    # With the already parsed activities and alternative subgraph data,
    # we add optional and selections groups data to the activities.
    activities = _make_optional_activities(activities, subgraphs)

    project = Project(list(range(len(activities))))
    return ProjectInstance(resources, activities, [project])


class DiGraph:
    """
    Simple directed graph implementation to replace networkx.DiGraph.
    """

    def __init__(self):
        self.adj: dict[int, list[int]] = defaultdict(list)
        self.nodes = set()

    def add_node(self, node: int):
        self.nodes.add(node)

    def add_edge(self, u: int, v: int):
        self.adj[u].append(v)
        self.nodes.add(u)
        self.nodes.add(v)

    def topological_sort(self) -> list[int]:
        """
        Returns a topological ordering of the graph's nodes.
        """
        in_degree = {node: 0 for node in self.nodes}
        for u in self.adj:
            for v in self.adj[u]:
                in_degree[v] += 1

        queue = deque(node for node in self.nodes if in_degree[node] == 0)
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self.adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return order

    @classmethod
    def from_activities(cls, activities: list[Activity]):
        G = cls()
        for idx, activity in enumerate(activities):
            G.add_node(idx)
            for succ in activity.successors:
                G.add_edge(idx, succ)

        return G


def _make_optional_activities(
    activities: list[Activity],
    subgraphs: list[AlternativeSubgraph],
) -> list[Activity]:
    """
    Adds optional and selection group data to activities based on alternative
    subgraph data. Because the activity graphs are directed acylcic, we can
    transform subgraphs into selection groups.
    """
    G = DiGraph.from_activities(activities)
    order = G.topological_sort()

    is_fixed = subgraphs[0].branches[0]  # first subgraph contains fixed nodes
    alternatives = subgraphs[1:]
    all_branching = []  # idcs of branching activities
    groups = defaultdict(list)

    for subgraph in alternatives:
        # The branching activities are the lowest-indexed activities in each
        # branch. This works because we have a directed acyclic graph.
        branching = [min(b, key=order.index) for b in subgraph.branches]
        arcs = [(u, v) for u in G.adj for v in G.adj[u] if v in branching]

        # The principal activity is the sole activity that goes to the
        # branching activities.
        nodes = {u for (u, _) in arcs}
        assert len(nodes) == 1  # should be only 1 principal activity
        principal = nodes.pop()

        all_branching.extend(branching)
        groups[principal].append(branching)

    # For all remaining edges, we add another unit selection group if
    # v is not a branching activity. Edges with v as a branching activity
    # are already covered by the groups above.
    for u in G.adj:
        for v in G.adj[u]:
            if v not in all_branching:
                groups[u].append([v])

    # Create new activities with optional and selection group data.
    new = []
    for idx, activity in enumerate(activities):
        activity = Activity(
            modes=activity.modes,
            successors=activity.successors,
            optional=idx not in is_fixed,
            selection_groups=groups[idx],
        )
        new.append(activity)

    for activity in new:
        # Check: In RCPSP-AS, timing successors are also selection successors.
        select_succ = list(chain(*activity.selection_groups))
        assert sorted(select_succ) == sorted(activity.successors)

    return new
