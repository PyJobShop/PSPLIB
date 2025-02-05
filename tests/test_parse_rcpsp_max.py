from numpy.testing import assert_equal

from psplib import parse_rcpsp_max

from .utils import relative


def test_ubo10():
    """
    Tests that the instance ``UBO10_01.rcpsp`` is correctly parsed.
    """
    instance = parse_rcpsp_max(relative("data/UBO10_01.sch"))

    capacities = [res.capacity for res in instance.resources]
    renewables = [res.renewable for res in instance.resources]

    assert_equal(instance.num_resources, 5)
    assert_equal(capacities, [10, 10, 10, 10, 10])
    assert_equal(renewables, [True, True, True, True, True])

    assert_equal(instance.num_activities, 12)

    activity = instance.activities[2]  # third activity
    assert_equal(activity.successors, [4, 11, 7])
    assert_equal(activity.delays, [5, 9, 0])

    assert_equal(activity.num_modes, 1)
    assert_equal(activity.modes[0].demands, [10, 8, 0, 8, 10])
    assert_equal(activity.modes[0].duration, 9)

    assert_equal(instance.num_projects, 1)
    assert_equal(instance.projects[0].num_activities, 12)
