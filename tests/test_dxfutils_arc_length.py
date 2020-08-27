from calculator.dxfutils import get_arc_length


def test_get_arc_length_angle_equal_180():
    # angle = 180 degree
    p1 = (0, 0, 0, 0, 1.0)
    p2 = (5, 0, 0, 0, 0)
    arc_length = round(get_arc_length(p1, p2), 7)

    assert arc_length == 7.8539816


def test_get_arc_length_angle_less_180_1():
    # angle less than 180 degree
    p1 = (3.0, 3.0, 0.0, 0.0, 0.25)
    p2 = (4.0, 4.0, 0.0, 0.0, 0.0)
    arc_length = round(get_arc_length(p1, p2), 7)

    assert arc_length == 1.4724216


def test_get_arc_length_angle_less_180_2():
    # angle less than 180 degree
    p1 = (0, 0, 0, 0, 0.25)
    p2 = (3, 4, 0, 0, 0)
    arc_length = round(get_arc_length(p1, p2), 7)

    assert arc_length == 5.2057966


def test_get_arc_length_angle_greater_180_1():
    # angle greater than 180 degree
    p1 = (118.4, 84.75, 0.0, 0.0, 3.4)
    p2 = (111, 84.75, 0.0, 0.0, 0.0)
    arc_length = round(get_arc_length(p1, p2), 7)

    assert arc_length == 25.5436223


def test_get_arc_length_greater_180_2():
    # angle greater than 180 degree
    p1 = (0, 0, 0.0, 0.0, 3.25)
    p2 = (3, 4, 0.0, 0.0, 0.0)
    arc_length = round(get_arc_length(p1, p2), 7)

    assert arc_length == 28.1736254
