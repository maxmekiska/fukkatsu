from unittest.mock import MagicMock, patch

import pytest

from fukkatsu.revive.reanimate import resurrect

suggested_code = """
def my_function(x, y, z):
    if y == 0:
        return z
    else:
        return x / y + z
"""
suggested_code_fail0 = """
def my_function(x, y, z):
    if y == 0:
        retur z
    else:
        retur x / y + z
"""
suggested_code_fail1 = """
def my_function(x, y, z):
    if
"""

mock_values = [suggested_code_fail0, suggested_code_fail1, suggested_code]


def mock_generator():
    while mock_values:
        put = mock_values.pop(0)
        mock_values.append(put)
        yield put


def test_reanimate():
    @resurrect(lives=1)
    def my_function(x, y, z):
        if y == 0:
            return z
        else:
            return x / y + z

    assert my_function(1, 2, 3) == 3.5


def test_reanimate_one_correction_success():

    with patch("fukkatsu.revive.reanimate.defibrillate") as mock_defibrillate:
        mock_defibrillate.return_value = suggested_code

        @resurrect(lives=2)
        def my_function(x, y, z):
            return x / y + z

        assert my_function(1, 0, 3) == 3


def test_reanimate_three_correction_success():

    with patch("fukkatsu.revive.reanimate.defibrillate", side_effect=mock_generator()):

        @resurrect(lives=4)
        def my_function(x, y, z):
            return x / y + z

        assert my_function(1, 0, 3) == 3


def test_reanimate_two_failure():

    with patch("fukkatsu.revive.reanimate.defibrillate", side_effect=mock_generator()):

        @resurrect(lives=3)
        def my_function(x, y, z):
            return x / y + z

        with pytest.raises(Exception) as e:
            my_function(1, 0, 3)

        expected_error_msg = "|__|__|______ my_function flatlined"
        assert str(e.value) == expected_error_msg
