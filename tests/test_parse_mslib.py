from numpy.testing import assert_equal

from psplib import parse_mslib

from .utils import relative


def test_mslib_set1():
    """
    Tests that the instance ``MSLIB1_Set1_1.msrcp`` is correctly parsed.
    """
    instance = parse_mslib(relative("data/MSLIB_Set1_1.msrcp"))

    capacities = [res.capacity for res in instance.resources]
    renewables = [res.renewable for res in instance.resources]

    assert_equal(instance.num_resources, 4)
    assert_equal(capacities, [1, 1, 1, 1])
    assert_equal(renewables, [True, True, True, True])

    resource = instance.resources[0]
    assert_equal(resource.skills, [1, 1, 1, 1])

    assert_equal(instance.num_activities, 32)

    activity = instance.activities[1]

    assert_equal(activity.successors, [10, 14, 22, 23, 25, 26, 27, 28])
    assert_equal(activity.delays, None)
    assert_equal(activity.num_modes, 1)

    mode = activity.modes[0]
    assert_equal(activity.num_modes, 1)
    assert_equal(mode.demands, [0, 0, 0, 0])
    assert_equal(mode.duration, 7)
    assert_equal(mode.skill_requirements, [0, 3, 0, 0])

    assert_equal(instance.num_skills, 4)


def test_bug_resource_skills():
    """
    Tests that a bug where resources had the wrong skills is fixed.
    """
    instance = parse_mslib(relative("data/MSLIB_Set1_11.msrcp"))

    capacities = [res.capacity for res in instance.resources]
    renewables = [res.renewable for res in instance.resources]

    assert_equal(instance.num_resources, 9)
    assert_equal(capacities, [1] * 9)
    assert_equal(renewables, [True] * 9)

    resource = instance.resources[0]
    assert_equal(resource.skills, [1, 1, 0, 0])

    resource = instance.resources[2]
    assert_equal(resource.skills, [0, 1, 0, 0])
