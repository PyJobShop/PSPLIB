from dataclasses import dataclass, field
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
    optional
        Whether this activity is optional or not. Default ``False``.
    selection_groups
        The selection groups of this activity. If the current activity is
        scheduled, then for each group, exactly one activity must be scheduled.
        This is used for RCPSP-PS instances. Default is an empty list.
    name
        Optional name of the activity to identify this activity. This is
        helpful to map this activity back to the original problem instance.
    """

    modes: list[Mode]
    successors: list[int]
    delays: Optional[list[int]] = None
    optional: bool = False
    selection_groups: list[list[int]] = field(default_factory=list)
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

    Mainly used in multi-project instances. In regular project scheduling
    instances, there is only one project that contains all activities.

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
    The project scheduling instance.
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
