from pathlib import Path
from typing import Union

from .ProjectInstance import Activity, Mode, Project, ProjectInstance, Resource


def parse_rcpsp_ps(instance_loc: Union[str, Path]) -> ProjectInstance:
    """
    Parses a RCPSP-PS formatted instance from Van der Beek et al. (2024).
    """
    with open(instance_loc, "r") as fh:
        lines = iter(line.strip() for line in fh.readlines() if line.strip())

    num_activities, num_renewable, _ = map(int, next(lines).split())
    capacities = list(map(int, next(lines).split()))

    resources = [
        Resource(capacity, idx < num_renewable)  # resources are ordered
        for idx, capacity in enumerate(capacities)
    ]
    activities = []

    for idx in range(num_activities):
        duration, *demands = map(int, next(lines).split())
        line = map(int, next(lines).split())

        groups = []
        num_groups = next(line)
        for _ in range(num_groups):
            num_successors = next(line)
            groups.append([next(line) for _ in range(num_successors)])

        num_successors, *successors = map(int, next(lines).split())
        activities.append(
            Activity(
                [Mode(duration, demands)],
                successors,
                optional=idx > 0,  # source activity is not optional
                selection_groups=groups,
            )
        )

    project = Project(list(range(num_activities)))
    return ProjectInstance(resources, activities, [project])
