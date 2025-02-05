from numpy.testing import assert_equal

from psplib import parse_aslib

from .utils import relative


def test_aslib0_0():
    """
    Tests that the instance ``aslib0_0.rcp`` is correctly parsed.
    """
    instance = parse_aslib(relative("data/aslib0_0.rcp"))
    assert_equal(instance.num_resources, 5)

    capacities = [res.capacity for res in instance.resources]
    renewables = [res.renewable for res in instance.resources]

    assert_equal(capacities, [10, 10, 10, 10, 10])
    assert_equal(renewables, [True, True, True, True, True])

    assert_equal(instance.num_activities, 122)

    activity = instance.activities[0]  # source
    assert_equal(activity.successors, [1, 13, 25, 37, 49])
    assert_equal(activity.optional, False)  # source always present
    assert_equal(activity.selection_groups, [[1, 13, 25, 37, 49]])

    assert_equal(activity.num_modes, 1)
    assert_equal(activity.modes[0].demands, [0, 0, 0, 0, 0])
    assert_equal(activity.modes[0].duration, 0)

    activity = instance.activities[2]
    assert_equal(activity.successors, [9, 8])
    assert_equal(activity.optional, True)
    assert_equal(activity.selection_groups, [[9], [8]])

    assert_equal(activity.num_modes, 1)
    assert_equal(activity.modes[0].demands, [0, 0, 1, 0, 0])
    assert_equal(activity.modes[0].duration, 1)

    assert_equal(instance.num_projects, 1)
    assert_equal(instance.projects[0].num_activities, 122)
