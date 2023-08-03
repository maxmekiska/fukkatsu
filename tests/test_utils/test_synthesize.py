from unittest.mock import patch

import pytest

from fukkatsu.utils.synthesize import defibrillate, enhance, stalker, twin


def test_defibrillate_with_mock():
    inputs = "example input"
    faulty_function = "def foo(x): return x + 1"
    error_trace = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    model_api = "openai"
    config = {"model": "gpt", "temperature": 0.5}

    expected_corrected_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.llm.openaigate.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_corrected_function}}]
        }

        corrected_function = defibrillate(
            model_api=model_api,
            inputs=inputs,
            faulty_function=faulty_function,
            error_trace=error_trace,
            config=config,
        )

        assert corrected_function == expected_corrected_function


def test_enhance_with_mock():
    inputs = "example input"
    target_function = "def foo(x): return x + 1"
    request = "Enahnce the function"
    model_api = "openai"
    config = {"model": "gpt", "temperature": 0.5}

    expected_enhanced_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.llm.openaigate.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_enhanced_function}}]
        }

        corrected_function = enhance(
            model_api=model_api,
            inputs=inputs,
            target_function=target_function,
            request=request,
            config=config,
        )

        assert corrected_function == expected_enhanced_function


def test_twin_with_mock():
    inputs = "example input"
    target_function = "def foo(x): return x + 1"
    model_api = "openai"
    config = {"model": "gpt", "temperature": 0.5}

    expected_enhanced_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.llm.openaigate.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_enhanced_function}}]
        }

        corrected_function = twin(
            model_api=model_api,
            inputs=inputs,
            target_function=target_function,
            config=config,
        )

        assert corrected_function == expected_enhanced_function


def test_stalker_with_mock_no_additional_rquest():
    inputs = "example input"
    target_function = "def foo(x): return x + 1"
    additonal_request = ""
    model_api = "openai"
    config = {"model": "gpt", "temperature": 0.5}

    expected_enhanced_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.llm.openaigate.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_enhanced_function}}]
        }

        corrected_function = stalker(
            model_api=model_api,
            inputs=inputs,
            function=target_function,
            config=config,
            additional_req=additonal_request,
        )

        assert corrected_function == expected_enhanced_function


def test_stalker_with_mock_additional_rquest():
    inputs = "example input"
    target_function = "def foo(x): return x + 1"
    additonal_request = "Enhance the function"
    model_api = "openai"
    config = {"model": "gpt", "temperature": 0.5}

    expected_enhanced_function = "def foo(x):\n    return str(x) + '1'"

    with patch(
        "fukkatsu.llm.openaigate.openai.ChatCompletion.create"
    ) as mock_completion_create:
        mock_completion_create.return_value = {
            "choices": [{"message": {"content": expected_enhanced_function}}]
        }

        corrected_function = stalker(
            model_api=model_api,
            inputs=inputs,
            function=target_function,
            config=config,
            additional_req=additonal_request,
        )

        assert corrected_function == expected_enhanced_function
