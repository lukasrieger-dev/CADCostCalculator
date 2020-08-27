import pytest
from calculator.dxfutils import get_dxf_model_space, get_min_square


def test_get_min_square_square():
    path = './dxf/square.dxf'
    msp = get_dxf_model_space(path)

    # a = 10.0, b = 5.0 -> expected 50.0
    a, b, area = get_min_square(msp, offset=0)

    assert (a, b, area) == (10.0, 5.0, 50.0)


def test_get_min_square_square_offset():
    path = './dxf/square.dxf'
    msp = get_dxf_model_space(path)

    a, b, area = get_min_square(msp, offset=1)

    assert (a, b, area) == (12.0, 7.0, 84.0)


def test_get_min_square_triangle():
    path = './dxf/triangle.dxf'
    msp = get_dxf_model_space(path)

    # triangle: a = 10.0, b = 5.0 -> expected: 50.0
    a, b, area = get_min_square(msp, offset=0)

    assert (a, b, area) == (10.0, 5.0, 50.0)


def test_get_min_square_triangle_offset():
    path = './dxf/triangle.dxf'
    msp = get_dxf_model_space(path)

    a, b, area = get_min_square(msp, offset=1)

    assert (a, b, area) == (12.0, 7.0, 84.0)


def test_get_min_square_diamond():
    path = './dxf/diamond.dxf'
    msp = get_dxf_model_space(path)
    a, b, area = get_min_square(msp, offset=0)

    # diamond: (0, 5), (5, 0), (10, 5), (5, 10)
    assert (a, b, area) == (10.0, 10.0, 100.0)


def test_get_min_square_circle():
    path = './dxf/circle.dxf'
    msp = get_dxf_model_space(path)
    a, b, area = get_min_square(msp, offset=0)

    assert (a, b, area) == (8.0, 8.0, 64.0)


def test_get_min_square_circle_diamond():
    path = './dxf/circled_diamond.dxf'
    msp = get_dxf_model_space(path)
    a, b, area = get_min_square(msp, offset=0)

    assert (a, b, area) == (12.0, 10.0, 120.0)


def test_get_min_square_circle_diamond_with_text():
    path = './dxf/circled_diamond_with_text.dxf'
    msp = get_dxf_model_space(path)
    a, b, area = get_min_square(msp, offset=0)

    # text must be ignored
    assert (a, b, area) == (12.0, 10.0, 120.0)


def test_get_min_square_unknown_element():
    path = './dxf/cube_mesh.dxf'
    with pytest.raises(ValueError):
        msp = get_dxf_model_space(path)
        get_min_square(msp, offset=0)


def test_get_min_square_negative_offset():
    path = './dxf/triangle.dxf'
    msp = get_dxf_model_space(path)

    # negative offsets must be ignored
    a, b, area = get_min_square(msp, offset=-3)

    assert (a, b, area) == (10.0, 5.0, 50.0)
