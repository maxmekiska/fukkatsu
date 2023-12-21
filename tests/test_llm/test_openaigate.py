from unittest.mock import Mock, patch

import pytest

from fukkatsu.llm.openaigate import request_openai_model


@pytest.fixture
def mock_openai_create():

    with patch("fukkatsu.llm.openaigate.openai.ChatCompletion.create") as mock_create:
        yield mock_create


@pytest.fixture
def mock_track_warning():
    with patch("fukkatsu.observer.tracker.track.warning") as mock_warning:
        yield mock_warning


def test_request_openai_model(mock_openai_create, mock_track_warning):
    set_prompt = "Test prompt"
    model = "gpt-3.5-turbo"
    temperature = 0.1
    max_tokens = 1024
    n = 1
    stop = None

    mock_openai_response = {"choices": [{"message": {"content": "Test response"}}]}

    mock_openai_create.return_value = mock_openai_response

    result = request_openai_model(
        set_prompt=set_prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
    )

    mock_track_warning.assert_called_once_with(
        f"API REQUEST to {model} - Temperature: {temperature} - Max Tokens: {max_tokens} - N: {n} - Stop: {stop}"
    )

    mock_openai_create.assert_called_once_with(
        model=model,
        messages=[
            {"role": "system", "content": set_prompt},
        ],
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
    )

    assert result == "Test response"
