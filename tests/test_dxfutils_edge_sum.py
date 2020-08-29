from calculator.dxfutils import get_dxf_model_space, get_edge_sum
from converter.converter import to_dxf_file


def test_get_edge_sum_of_converted():
    path_original_geo = './dxf/original_input.GEO'
    path_converted = './dxf/converted_result.dxf'
    path_original = './dxf/original.dxf'

    to_dxf_file(path_original_geo, path_converted)

    msp_converted = get_dxf_model_space(path_converted)
    msp_original = get_dxf_model_space(path_original)

    sum_converted = get_edge_sum(msp_converted)
    sum_original = get_edge_sum(msp_original)

    assert sum_original == sum_converted
