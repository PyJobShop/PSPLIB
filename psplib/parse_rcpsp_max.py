from pathlib import Path
from typing import Union

from .ProjectInstance import Activity, Mode, Project, ProjectInstance, Resource


def parse_rcpsp_max(loc: Union[str, Path]) -> ProjectInstance:
    """
    Parses the RCPSP/max instance format.

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

    num_activities, num_renewables, *_ = map(int, next(lines).split())
    num_activities += 2  # source and target
    activities = []

    succ_lines = [next(lines).split() for _ in range(num_activities)]
    activity_lines = [next(lines).split() for _ in range(num_activities)]

    for idx in range(num_activities):
        _, _, num_successors, *succ = succ_lines[idx]
        successors = list(map(int, succ[: int(num_successors)]))
        delays = [int(val.strip("[]")) for val in succ[int(num_successors) :]]

        _, _, duration, *demands = map(int, activity_lines[idx])

        activity = Activity([Mode(duration, demands)], successors, delays)
        activities.append(activity)

    capacities = map(int, next(lines).split())
    resources = [Resource(capacity, renewable=True) for capacity in capacities]
    projects = [Project(list(range(num_activities)))]

    return ProjectInstance(resources, activities, projects)
