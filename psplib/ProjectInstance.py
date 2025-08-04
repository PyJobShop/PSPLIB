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
    skills
        Whether the resource has a skill or not. Default is ``None``,
        which means that there are no skills considered.
    """

    capacity: int
    renewable: bool
    skills: Optional[list[bool]] = None


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
    skill_requirements
        The skill requirements (one per skill) of this processing mode,
        if applicable.
    """

    duration: int
    demands: list[int]
    skill_requirements: Optional[list[int]] = None


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
        scheduled, then for each group at least one activity must be scheduled.
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
    due_date
        The due date of this project, if available. Default is ``None``.
    """

    activities: list[int]
    release_date: int = 0
    due_date: Optional[int] = None

    @property
    def num_activities(self):
        return len(self.activities)


@dataclass
class ProjectInstance:
    """
    The project scheduling instance.

    Parameters
    ----------
    resources
        The resources available in the instance.
    activities
        The activities that need to be scheduled.
    projects
        The projects that contain the activities.
    skills
        The skills that are available in the instance. Default is ``None``,
        which means that the instance does not consider skills.
    """

    resources: list[Resource]
    activities: list[Activity]
    projects: list[Project]
    skills: Optional[list[int]] = None

    @property
    def num_resources(self):
        return len(self.resources)

    @property
    def num_activities(self):
        return len(self.activities)

    @property
    def num_projects(self):
        return len(self.projects)

    @property
    def num_skills(self):
        return len(self.skills) if self.skills else 0

    def __post_init__(self):
        for activity in self.activities:
            for mode in activity.modes:
                if (
                    mode.skill_requirements is not None
                    and len(mode.skill_requirements) != self.num_skills
                ):
                    msg = "Skill requirements does not match number of skills."
                    raise ValueError(msg)

        for resource in self.resources:
            if (
                resource.skills is not None
                and len(resource.skills) != self.num_skills
            ):
                msg = "Resource skills does not match number of skills."
                raise ValueError(msg)
