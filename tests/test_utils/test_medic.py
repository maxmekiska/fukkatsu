from unittest.mock import patch

import pytest

from fukkatsu.utils.medic import defibrillate


def test_defibrillate_with_mock():
    inputs = "example input"
    faulty_function = "def foo(x): return x + 1"
    error_trace = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"

    expected_corrected_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.utils.medic.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_corrected_function}}]
        }

        corrected_function = defibrillate(inputs, faulty_function, error_trace)

        assert corrected_function == expected_corrected_function
