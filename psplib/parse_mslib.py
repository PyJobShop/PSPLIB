from pathlib import Path
from typing import Union

from .ProjectInstance import Activity, Mode, Project, ProjectInstance, Resource


def parse_mslib(loc: Union[str, Path]) -> ProjectInstance:
    """
    Parses a MS-RCPSP formatted instance from Snauwaert and Vanhoucke (2023).
    """
    with open(loc, "r") as fh:
        lines = iter(line.strip() for line in fh.readlines() if line.strip())

    # Project module.
    next(lines)
    num_activities, num_resources, _, _ = map(int, next(lines).split())
    next(lines)  # deadline
    next(lines)  # deadline skill level requirement

    durations = []
    successors = []
    for _ in range(num_activities):
        line = iter(map(int, next(lines).split()))
        durations.append(int(next(line)))

        # Succesors are 1-indexed.
        num_successors = int(next(line))
        successors.append([int(next(line)) - 1 for _ in range(num_successors)])

    # Workforce module.
    next(lines)
    resource_skills = [
        list(map(bool, next(lines).split())) for _ in range(num_resources)
    ]

    # Workforce module with skill levels.
    next(lines)
    [next(lines) for _ in range(num_resources)]

    # Skill requirements module.
    next(lines)
    skill_reqs = [
        list(map(int, next(lines).split())) for _ in range(num_activities)
    ]

    # All other lines are for extensions to MSRCPSP.
    skills = list(range(len(resource_skills[0])))

    # Resources always have capacity 1 because they can only process one
    # activity at a time.
    resources = [
        Resource(capacity=1, renewable=True, skills=skills)
        for skills in resource_skills
    ]

    activities = [
        Activity(
            modes=[
                Mode(
                    duration=durations[idx],
                    demands=[0] * num_resources,  # ignore this demand
                    skill_requirements=skill_reqs[idx],
                )
            ],
            successors=successors[idx],
        )
        for idx in range(num_activities)
    ]

    project = Project(list(range(len(activities))))
    return ProjectInstance(resources, activities, [project], skills)
