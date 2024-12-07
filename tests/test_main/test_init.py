from unittest.mock import patch

import pytest

from fukkatsu import mutate, reset_memory, resurrect, stalk

suggested_code = """
|||def my_function(x, y, z):
    if y == 0:
        return z
    else:
        return x / y + z|||
"""
suggested_code_fail0 = """
|||def my_function(x, y, z):
    if y == 0:
        return x/y + y + z
    else:
        retur x / y + z|||
"""
suggested_code_fail1 = """
|||def my_function(x, y, z):
    return x / y|||
"""

suggested_code_fail2 = """
|||def my_function(x, y, z):
    return x / y + z + z|||
"""

suggested_code_fail3 = """
|||def my_function(x, y, z):
    return x / y + y|||
"""

suggested_code_dummy = """
|||def my_function(x, y, z):
    print("success")|||
"""

mock_values0 = [suggested_code_fail0, suggested_code_fail1, suggested_code]
mock_values1 = [
    suggested_code_fail0,
    suggested_code_fail1,
    suggested_code_fail1,
    suggested_code,
]
mock_values2 = [suggested_code_fail2, suggested_code_fail3, suggested_code]
mock_values3 = suggested_code


def mock_generator(mock_values):
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

    with patch("fukkatsu.defibrillate") as mock_defibrillate:
        mock_defibrillate.return_value = suggested_code

        @resurrect(lives=1)
        def my_function(x, y, z):
            return x / y + z

        assert my_function(1, 0, 3) == 3


def test_reanimate_inmemory_success1():

    with patch(
        "fukkatsu.defibrillate",
        side_effect=mock_generator(mock_values0),
    ):

        @resurrect(lives=2)
        def my_function(x, y, z):
            return x / y + z

        assert my_function(1, 0, 3) == 3


def test_reanimate_inmemory_success2():

    with patch(
        "fukkatsu.defibrillate",
        side_effect=mock_generator(mock_values1),
    ):

        @resurrect(lives=2)
        def my_function(x, y, z):
            return x / y + z

        assert my_function(1, 0, 3) == 3


def test_reanimate_failure():

    with patch(
        "fukkatsu.defibrillate",
        side_effect=mock_generator(mock_values2),
    ):

        @resurrect(lives=2)
        def my_function(x, y, z):
            return x + z / y

        with pytest.raises(Exception) as e:
            my_function(1, 0, 3)

        expected_error_msg = "|__|__|______ my_function flatlined"
        assert str(e.value) == expected_error_msg


def test_reanimate_three_correction_success():

    with patch(
        "fukkatsu.defibrillate",
        side_effect=mock_generator(mock_values2),
    ):

        @resurrect(lives=4)
        def my_function(x, y, z):
            return x + z / y

        assert my_function(1, 0, 3) == 3


def test_reanimate_twin():

    with patch("fukkatsu.defibrillate") as mock_enhance:
        mock_enhance.return_value = suggested_code

        with patch("fukkatsu.twin") as mock_twin:
            mock_twin.return_value = suggested_code

            @resurrect(lives=1, active_twin=True)
            def my_function(x, y, z):
                return x / y + z

            assert my_function(1, 0, 3) == 3


def test_mutate():

    with patch("fukkatsu.enhance") as mock_enhance:
        mock_enhance.return_value = suggested_code

        @mutate(request="Test Request")
        def my_function(x, y, z):
            return x / y + z

        assert my_function(1, 0, 3) == 3


def test_mutate_twin():

    with patch("fukkatsu.enhance") as mock_enhance:
        mock_enhance.return_value = suggested_code

        with patch("fukkatsu.twin") as mock_twin:
            mock_twin.return_value = suggested_code

            @mutate(request="Test Request", active_twin=True)
            def my_function(x, y, z):
                return x / y + z

            assert my_function(1, 0, 3) == 3


def test_stalk():

    with patch("fukkatsu.stalker") as mock_enhance:
        mock_enhance.return_value = suggested_code

        @stalk(likelihood=1.0, active_twin=False)
        def my_function(x, y, z):
            return x / y + z

        assert my_function(1, 0, 3) == 3


def test_stalk_twin():

    with patch("fukkatsu.stalker") as mock_enhance:
        mock_enhance.return_value = suggested_code

        with patch("fukkatsu.twin") as mock_twin:
            mock_twin.return_value = suggested_code

            @stalk(likelihood=1.0, active_twin=True)
            def my_function(x, y, z):
                return x / y + z

            assert my_function(1, 0, 3) == 3


def test_reanimate_human_input_accepted():

    with patch(
        "fukkatsu.defibrillate",
        side_effect=mock_values3,
    ):

        with patch("fukkatsu.human_decision") as mock_decision:
            mock_decision.return_value = True

            @resurrect(lives=1, human_action=True)
            def my_function(x, y, z):
                return x / y + z

            assert my_function(1, 0, 3) == 3


def test_reanimate_human_input_rejected():

    with patch(
        "fukkatsu.defibrillate",
        side_effect=mock_values3,
    ):

        with patch("fukkatsu.human_decision") as mock_decision:
            mock_decision.return_value = False

            @resurrect(lives=1, human_action=True)
            def my_function(x, y, z):
                return x / y + z

            with pytest.raises(Exception) as e:
                my_function(1, 0, 3)

            expected_error_msg = "|__|__|______ my_function flatlined"
            assert str(e.value) == expected_error_msg


def test_mutate_human_accepted():

    with patch("fukkatsu.enhance") as mock_enhance:
        mock_enhance.return_value = suggested_code

        with patch("fukkatsu.human_decision") as mock_decision:
            mock_decision.return_value = True

            @mutate(request="Test Request", human_action=True)
            def my_function(x, y, z):
                return x / y + z

            assert my_function(1, 0, 3) == 3


def test_mutate_human_rejection():

    with patch("fukkatsu.enhance") as mock_enhance:
        mock_enhance.return_value = suggested_code

        with patch("fukkatsu.human_decision") as mock_decision:
            mock_decision.return_value = False

            @mutate(request="Test Request", human_action=True)
            def my_function(x, y, z):
                return x / y + z

            with pytest.raises(Exception) as e:
                my_function(1, 0, 3)

            expected_error_msg = "Human rejected mutation. Terminating\n"
            assert str(e.value) == expected_error_msg


def test_stalk_human_accepted():

    with patch("fukkatsu.stalker") as mock_enhance:
        mock_enhance.return_value = suggested_code

        with patch("fukkatsu.human_decision") as mock_decision:
            mock_decision.return_value = True

            @stalk(likelihood=1.0, active_twin=False, human_action=True)
            def my_function(x, y, z):
                return x / y + z

            assert my_function(1, 0, 3) == 3


def test_stalk_human_rejection():

    with patch("fukkatsu.stalker") as mock_enhance:
        mock_enhance.return_value = suggested_code

        with patch("fukkatsu.human_decision") as mock_decision:
            mock_decision.return_value = False

            @stalk(likelihood=1.0, active_twin=False, human_action=True)
            def my_function(x, y, z):
                return x / y + z

            with pytest.raises(Exception) as e:
                my_function(1, 0, 3)

            expected_error_msg = "Human rejected suggestion. Terminating\n"
            assert str(e.value) == expected_error_msg


def test_reanimation_memory_off_human_yes():

    with patch("fukkatsu.defibrillate") as mock_defibrillate, patch(
        "fukkatsu.human_decision"
    ) as mock_human_input:
        mock_defibrillate.return_value = suggested_code
        mock_human_input.return_value = True

        @resurrect(lives=1, active_memory=False, human_action=True)
        def my_function(x, y, z):
            return x / y + z

        assert my_function(1, 0, 3) == 3


def test_reanimation_memory_on_human_yes():

    with patch("fukkatsu.defibrillate") as mock_defibrillate, patch(
        "fukkatsu.human_decision"
    ) as mock_human_input:
        mock_defibrillate.return_value = suggested_code
        mock_human_input.return_value = True

        @resurrect(lives=1, active_memory=True, human_action=True)
        def my_function(x, y, z):
            return x / y + z

        assert my_function(1, 0, 3) == 3


def test_reanimation_memory_off_human_no():

    with patch("fukkatsu.defibrillate") as mock_defibrillate, patch(
        "fukkatsu.human_decision"
    ) as mock_human_input:
        mock_defibrillate.return_value = suggested_code
        mock_human_input.return_value = False

        @resurrect(lives=1, active_memory=False, human_action=True)
        def my_function(x, y, z):
            return x / y + z

        with pytest.raises(Exception) as e:
            my_function(1, 0, 3)

        expected_error_msg = "|__|__|______ my_function flatlined"
        assert str(e.value) == expected_error_msg
