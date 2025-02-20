from numpy.testing import assert_equal

from psplib import parse_rcpsp_ps

from .utils import relative


def test_rcpsp_ps():
    """
    Tests that the instance ``rcpsp_ps.txt`` is correctly parsed.
    """
    instance = parse_rcpsp_ps(relative("data/rcpsp_ps.txt"))

    assert_equal(instance.num_resources, 4)

    capacities = [res.capacity for res in instance.resources]
    renewables = [res.renewable for res in instance.resources]

    assert_equal(capacities, [10, 10, 10, 10])
    assert_equal(renewables, [True, True, True, True])

    assert_equal(instance.num_activities, 136)

    activity = instance.activities[0]  # first activity (source)
    assert_equal(activity.successors, [1, 2])
    assert_equal(activity.optional, False)  # source always present
    assert_equal(activity.selection_groups, [[1, 2]])

    assert_equal(activity.num_modes, 1)
    assert_equal(activity.modes[0].demands, [0, 0, 0, 0])
    assert_equal(activity.modes[0].duration, 0)

    activity = instance.activities[3]  # fourth activity
    assert_equal(activity.successors, [5])
    assert_equal(activity.selection_groups, [[5]])

    assert_equal(activity.num_modes, 1)
    assert_equal(activity.modes[0].demands, [0, 0, 1, 1])
    assert_equal(activity.modes[0].duration, 9)

    assert_equal(instance.num_projects, 1)
    assert_equal(instance.projects[0].num_activities, 136)
