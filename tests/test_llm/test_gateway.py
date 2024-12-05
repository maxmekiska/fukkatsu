from unittest.mock import MagicMock, patch

import pytest

from fukkatsu.llm.gateway import request_model


@pytest.fixture
def mock_openai_client():
    with patch("fukkatsu.llm.gateway.OpenAI") as mock_openai:
        yield mock_openai


@pytest.fixture
def mock_track_warning():
    with patch("fukkatsu.observer.tracker.track.warning") as mock_warning:
        yield mock_warning


def test_request_model(mock_openai_client, mock_track_warning):
    set_prompt = "Test prompt"
    model = "model"
    temperature = 0.1
    max_tokens = 1024
    n = 1
    stop = None

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]

    mock_openai_instance = mock_openai_client.return_value
    mock_openai_instance.chat.completions.create.return_value = mock_response

    result = request_model(
        set_prompt=set_prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
    )

    mock_track_warning.assert_any_call(
        f"API REQUEST to {model} - Temperature: {temperature} - Max Tokens: {max_tokens} - N: {n} - Stop: {stop}"
    )
    mock_track_warning.assert_any_call(mock_response)

    mock_openai_instance.chat.completions.create.assert_called_once_with(
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
