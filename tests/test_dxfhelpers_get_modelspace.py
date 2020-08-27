import pytest
from calculator.dxfhelpers import *


def test_get_dxf_modelspace():
    path = './dxf/square.dxf'
    msp = get_dxf_model_space(path)

    assert msp


def test_get_dxf_modelspace_not_found():
    with pytest.raises(FileNotFoundError):
        path = './invalid/path'
        get_dxf_model_space(path)