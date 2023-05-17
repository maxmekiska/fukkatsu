import re

import pytest

from fukkatsu.utils.helper import *


@pytest.mark.parametrize(
    "input_str, expected_output_str",
    [
        (
            "This is a test string without any trace lines",
            "This is a test string without any trace lines",
        ),
        (
            "Traceback (most recent call last):\n File 'example.py', line 5, in <module>\n   print('Hello, World!')\nNameError: name 'print' is not defined\n",
            "Traceback (most recent call last):\n File 'example.py', , in <module>\n   print('Hello, World!')\nNameError: name 'print' is not defined\n",
        ),
        (
            "Traceback (most recent call last):\n File 'example.py', line 5, in <module>\n   print('Hello, World!')\nNameError: name 'print' is not defined\n\nTraceback (most recent call last):\n File 'example.py', line 8, in <module>\n   main()\nNameError: name 'main' is not defined\n",
            "Traceback (most recent call last):\n File 'example.py', , in <module>\n   print('Hello, World!')\nNameError: name 'print' is not defined\n\nTraceback (most recent call last):\n File 'example.py', , in <module>\n   main()\nNameError: name 'main' is not defined\n",
        ),
        ("", ""),
    ],
)
def test_remove_trace_lines(input_str, expected_output_str):
    assert remove_trace_lines(input_str) == expected_output_str


@pytest.mark.parametrize(
    "input_str, expected_output_str",
    [
        (
            "@test\ndef add(x, y):\n    return x + y\n",
            "def add(x, y):\n    return x + y\n",
        ),
        (
            "def divide(x, y):\n    return x / y\n",
            "def divide(x, y):\n    return x / y\n",
        ),
    ],
)
def test_remove_wrapper_name(input_str, expected_output_str):
    assert remove_wrapper_name(input_str) == expected_output_str


@pytest.mark.parametrize(
    "message, expected_output_str",
    [
        ("Some text before |||some code||| and some text after.", "some code"),
        ("This message doesn't contain backticks.", ""),
        ("A single backtick `is` not enough to extract text.", ""),
        (
            "Backticks must be on their own line to be extracted:\n|||some code|||",
            "some code",
        ),
    ],
)
def test_extract_text_between_backticks(message, expected_output_str):
    assert extract_text_between_backticks(message) == expected_output_str


def example_function(x, y):
    return x + y


def test_return_source_code():

    expected_output_str = "def example_function(x, y):\n    return x + y\n"

    assert return_source_code(example_function) == expected_output_str


def test_return_input_arguments():

    expected_output_dict = {"x": 1, "y": 2}

    assert return_input_arguments(example_function, 1, 2) == expected_output_dict
