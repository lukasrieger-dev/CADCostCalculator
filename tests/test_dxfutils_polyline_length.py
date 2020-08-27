from calculator.dxfutils import get_dxf_model_space, get_polyline_length


def test_get_length_simple_polyline():
    path = './dxf/simple_polyline.dxf'
    msp = get_dxf_model_space(path)

    polyline = msp[0]
    length = round(get_polyline_length(polyline), 7)

    assert length == 12.3851648


def test_get_length_complex_polyline():
    path = './dxf/complex_polyline.dxf'
    msp = get_dxf_model_space(path)

    polyline = msp[0]
    length = round(get_polyline_length(polyline), 7)

    assert length == 17.9955743


