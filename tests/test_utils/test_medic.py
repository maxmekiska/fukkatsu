import io
import logging
import os
import sys
from unittest.mock import patch

import openai
import pytest

from fukkatsu.observer.tracker import track
from fukkatsu.utils.medic import (defibrillate, enhance, overwrite_openai_key,
                                  set_openai_key, stalker, twin)


@pytest.fixture
def captured_output():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    yield captured_output
    sys.stdout = sys.__stdout__


def test_defibrillate_with_mock():
    inputs = "example input"
    faulty_function = "def foo(x): return x + 1"
    error_trace = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    llm = {"primary": "gpt"}
    temperature = {"primary": 0.5}

    expected_corrected_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.utils.medic.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_corrected_function}}]
        }

        corrected_function = defibrillate(
            inputs, faulty_function, error_trace, llm["primary"], temperature["primary"]
        )

        assert corrected_function == expected_corrected_function


def test_enhance_with_mock():
    inputs = "example input"
    target_function = "def foo(x): return x + 1"
    request = "Enahnce the function"
    llm = {"primary": "gpt"}
    temperature = {"primary": 0.5}

    expected_enhanced_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.utils.medic.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_enhanced_function}}]
        }

        corrected_function = enhance(
            inputs, target_function, request, llm["primary"], temperature["primary"]
        )

        assert corrected_function == expected_enhanced_function


def test_twin_with_mock():
    inputs = "example input"
    target_function = "def foo(x): return x + 1"
    llm = {"primary": "gpt"}
    temperature = {"primary": 0.5}

    expected_enhanced_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.utils.medic.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_enhanced_function}}]
        }

        corrected_function = twin(
            inputs, target_function, llm["primary"], temperature["primary"]
        )

        assert corrected_function == expected_enhanced_function


def test_stalker_with_mock_no_additional_rquest():
    inputs = "example input"
    target_function = "def foo(x): return x + 1"
    additonal_request = ""
    llm = {"primary": "gpt"}
    temperature = {"primary": 0.5}

    expected_enhanced_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.utils.medic.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_enhanced_function}}]
        }

        corrected_function = stalker(
            inputs=inputs,
            function=target_function,
            model=llm["primary"],
            temperature=temperature["primary"],
            additional_req=additonal_request,
        )

        assert corrected_function == expected_enhanced_function


def test_stalker_with_mock_additional_rquest():
    inputs = "example input"
    target_function = "def foo(x): return x + 1"
    additonal_request = "Enhance the function"
    llm = {"primary": "gpt"}
    temperature = {"primary": 0.5}

    expected_enhanced_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.utils.medic.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_enhanced_function}}]
        }

        corrected_function = stalker(
            inputs=inputs,
            function=target_function,
            model=llm["primary"],
            temperature=temperature["primary"],
            additional_req=additonal_request,
        )

        assert corrected_function == expected_enhanced_function


def test_set_openai_key_with_api_key():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        set_openai_key()
        assert openai.api_key == "test_key"
        assert "OPENAI_API_KEY" in os.environ


def test_set_openai_key_without_api_key(captured_output):
    handler = logging.StreamHandler(captured_output)
    track.addHandler(handler)
    with patch("os.environ.get") as import_module_mock:
        import_module_mock.side_effect = Exception
        set_openai_key()
        output = captured_output.getvalue().strip()
        assert "OPENAI_API_KEY not found" in output


def test_overwrite_openai_key():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        overwrite_openai_key("new_key")
        assert openai.api_key == "new_key"


def test_overwrite_openai_key_error():
    with pytest.raises(
        Exception, match="Invalid Key format. OPENAI_API_KEY not overwritten."
    ):
        overwrite_openai_key(23)
