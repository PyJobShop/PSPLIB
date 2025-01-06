from dataclasses import dataclass
from typing import Optional


@dataclass
class Resource:
    """
    Resource class.

    Parameters
    ----------
    capacity
        The available maximum capacity of the resource.
    renewable
        Whether the resource is renewable or not.
    """

    capacity: int
    renewable: bool


@dataclass
class Mode:
    """
    Mode class.

    Parameters
    ----------
    duration
        The duration of this processing mode.
    demands
        The resource demands (one per resource) of this processing mode.
    """

    duration: int
    demands: list[int]


@dataclass
class Activity:
    """
    Activity class.

    Parameters
    ----------
    modes
        The processing modes of this activity.
    successors
        The indices of successor activities.
    delays
        The delay for each successor activity. If delays are specified, then
        the length of this list must be equal to the length of `successors`.
        Delays are used for RCPSP/max instances, where the precedence
        relationship is defined as ``start(pred) + delay <= start(succ)``.
    name
        Optional name of the activity to identify this activity. This is
        helpful to map this activity back to the original problem instance.
    """

    modes: list[Mode]
    successors: list[int]
    delays: Optional[list[int]] = None
    name: str = ""

    def __post_init__(self):
        if self.delays and len(self.delays) != len(self.successors):
            raise ValueError("Length of successors and delays must be equal.")

    @property
    def num_modes(self):
        return len(self.modes)


@dataclass
class Project:
    """
    A project is a collection of activities that share a common release date
    and the project is considered finished when all activities are completed.

    Parameters
    ----------
    activities
        The activities indices that belong to this project.
    release_date
        The earliest start time of this project.
    """

    activities: list[int]
    release_date: int = 0

    @property
    def num_activities(self):
        return len(self.activities)


@dataclass
class ProjectInstance:
    """
    Multi-project multi-mode resource-constrained project scheduling instance.
    """

    resources: list[Resource]
    activities: list[Activity]
    projects: list[Project]

    @property
    def num_resources(self):
        return len(self.resources)

    @property
    def num_activities(self):
        return len(self.activities)

    @property
    def num_projects(self):
        return len(self.projects)
