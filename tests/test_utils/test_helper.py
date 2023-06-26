import re
from unittest.mock import patch

import pytest

from fukkatsu.utils.helper import *

example_code_one = """import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
from fukkatsu.uitls import test

def my_mutated_function(x, y):
    '''
    This function prints 'Nice weather' if called with any inputs. If x is an even integer, a random matplotlib plot is created. If y is odd, a numpy array is created.
    '''
    print("Nice weather")
    if x % 2 == 0:
        plt.plot([random.random() for i in range(10)])
        plt.show()
    if y % 2 != 0:
        np_array = np.array([1, 2, 3])
        print(np_array)
"""

example_code_two = """import numpy as np
import matplotlib.pyplot as plt

import random


import pandas as pd

from fukkatsu.uitls import test
def my_mutated_function(x, y):
    '''
    This function prints 'Nice weather' if called with any inputs. If x is an even integer, a random matplotlib plot is created. If y is odd, a numpy array is created.
    '''
    print("Nice weather")
    if x % 2 == 0:
        plt.plot([random.random() for i in range(10)])
        plt.show()
    if y % 2 != 0:
        np_array = np.array([1, 2, 3])
        print(np_array)
"""


example_code_three = """def my_mutated_function(x, y):
    '''
    This function prints 'Nice weather' if called with any inputs. If x is an even integer, a random matplotlib plot is created. If y is odd, a numpy array is created.
    '''
    print("Nice weather")
    if x % 2 == 0:
        plt.plot([random.random() for i in range(10)])
        plt.show()
    if y % 2 != 0:
        np_array = np.array([1, 2, 3])
        print(np_array)
"""

example_insert_one = """def my_mutated_function(x, y):
    '''
    Testing.
    '''
    print("Nice weather")

my_mutated_function(2,2)
"""


example_code_imports_one = "    import numpy as np\n    import matplotlib.pyplot as plt\n    import random\n    import pandas as pd\n    from fukkatsu.uitls import test"
example_code_imports_two = "    import numpy as np\n    import matplotlib.pyplot as plt\n    import random\n    import pandas as pd\n    from fukkatsu.uitls import test"
example_code_imports_three = ""


example_inserted_function_one = """def my_mutated_function(x, y):
    import numpy as np
    import matplotlib.pyplot as plt
    import random
    import pandas as pd
    from fukkatsu.uitls import test
    '''
    Testing.
    '''
    print("Nice weather")

my_mutated_function(2,2)
"""


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
    assert extract_text_between_pipes(message) == expected_output_str


def example_function(x, y):
    return x + y


def test_return_source_code():

    expected_output_str = "def example_function(x, y):\n    return x + y\n"

    assert return_source_code(example_function) == expected_output_str


def test_return_input_arguments():

    expected_output_dict = {"x": 1, "y": 2}

    assert return_input_arguments(example_function, 1, 2) == expected_output_dict


@pytest.mark.parametrize(
    "input_str, expected_output_str",
    [
        (
            example_code_one,
            example_code_imports_one,
        ),
        (
            example_code_two,
            example_code_imports_two,
        ),
        (
            example_code_three,
            example_code_imports_three,
        ),
    ],
)
def test_extract_imports(input_str, expected_output_str):
    assert extract_imports(input_str) == expected_output_str


def test_insert_string_after_colon():
    assert (
        insert_string_after_colon(example_insert_one, example_code_imports_one)
        == example_inserted_function_one
    )


def test_insert_string_after_colon_no_change():
    assert (
        insert_string_after_colon("not matching string", "import pandas as pd")
        == "not matching string"
    )


@pytest.mark.parametrize(
    "message, expected_output_str",
    [
        ("python||def test():\npass", "|||def test():\npass"),
        ("python||def test()\npass", "|||def test()\npass"),
        ("|||def test()\npass|||", "|||def test()\npass|||"),
        ("def test()\npass|||", "def test()\npass|||"),
    ],
)
def test_standardize_delimiters(message, expected_output_str):
    assert standardize_delimiters(message) == expected_output_str


@pytest.mark.parametrize(
    "message, expected_output_str",
    [
        ("|||def test():\npass|||", "|||def test():\npass|||"),
        ("|||def test():\npass", "|||def test():\npass|||"),
        ("|||def test():\n    1 | 0", "|||def test():\n    1 | 0|||"),
    ],
)
def test_add_delimiters(message, expected_output_str):
    assert add_delimiters(message) == expected_output_str


@pytest.mark.parametrize(
    "likelihood, sample_answer",
    [
        (1.0, True),
        (0.0, False),
    ],
)
def test_sampler(likelihood, sample_answer):
    assert sampler(likelihood) == sample_answer


@pytest.mark.parametrize(
    "function, new_name, expected_output_str",
    [
        (
            "def calculate_square(num):\n    return num ** 2",
            "nameTest",
            "def nameTest(num):\n    return num ** 2",
        ),
        (
            "def find_max_value(lst):\n    if len(lst) == 0:\n        return None\n    max_value = lst[0]\n    for num in lst:\n        if num > max_value:\n            max_value = num\n    return max_value",
            "nameTest",
            "def nameTest(lst):\n    if len(lst) == 0:\n        return None\n    max_value = lst[0]\n    for num in lst:\n        if num > max_value:\n            max_value = num\n    return max_value",
        ),
        (
            "def is_palindrome(word):\n    word = word.lower()\n    return word == word[::-1]",
            "nameTest",
            "def nameTest(word):\n    word = word.lower()\n    return word == word[::-1]",
        ),
    ],
)
def test_rename_function(function, new_name, expected_output_str):
    assert rename_function(function, new_name) == expected_output_str


def test_check_and_install_libraries_with_import_error():
    with patch("importlib.import_module") as import_module_mock:
        import_module_mock.side_effect = ImportError
    with patch("fukkatsu.utils.helper.install_libraries") as mock_install_libraries:
        mock_install_libraries.return_value = None
        check_and_install_libraries("import my_library")

    mock_install_libraries.assert_called_once()


def test_check_and_install_libraries_no_error():
    with patch("importlib.import_module") as mock_import_module, patch(
        "fukkatsu.utils.helper.install_libraries"
    ) as mock_install_libraries:
        mock_import_module.return_value = None
        check_and_install_libraries("import my_library")

    mock_install_libraries.assert_not_called()


def test_check_and_install_libraries_no_error_from_syntax():
    with patch("importlib.import_module") as mock_import_module, patch(
        "fukkatsu.utils.helper.install_libraries"
    ) as mock_install_libraries:
        mock_import_module.return_value = None
        check_and_install_libraries("from my_library import my_function")

    mock_install_libraries.assert_not_called()
