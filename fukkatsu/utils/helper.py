import ast
import importlib
import inspect
import random
import re
import subprocess
import sys
from typing import Callable

from fukkatsu.observer.tracker import track


def remove_trace_lines(trace_error: str) -> str:
    pattern = r"\b\w*line\s\d+\w*\b"
    output_str = re.sub(pattern, "", trace_error)
    return output_str


def remove_wrapper_name(source_code: str) -> str:
    start_index = source_code.index("def")
    source_code = source_code[start_index:]
    return source_code


def standardize_delimiters(code_block: str) -> str:
    pattern = r"\|*\s*(?:python):?\|*"
    return re.sub(pattern, "|||", code_block)


def add_delimiters(message: str) -> str:
    message = message.rstrip()
    if message.endswith("|||"):
        return message
    elif message.count("|||") == 2:
        return message
    else:
        return message + "|||"


def remove_patterns(input_string):
    pattern1 = r"\|\|\|"
    pattern2 = r"```"

    combined_pattern = f"{pattern1}|{pattern2}"

    result_string = re.sub(combined_pattern, "", input_string)

    return result_string


def extract_text_between_pipes(message: str) -> str:
    message = standardize_delimiters(message)
    message = add_delimiters(message)
    start_idx = message.find("|||") + 3
    end_idx = message.rfind("|||")
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        return ""
    message = message[start_idx:end_idx].strip()
    cleaned_message = remove_patterns(message)
    return cleaned_message


def return_source_code(func: Callable) -> str:
    source = inspect.getsource(func)
    return source


def return_input_arguments(func: Callable, *args, **kwargs) -> dict:
    signature = inspect.signature(func)
    bound_args = signature.bind(*args, **kwargs)
    input_args = {k: bound_args.arguments[k] for k in signature.parameters.keys()}
    return input_args


def extract_imports(code_block: str) -> str:
    """Extract all import statements from a code block."""
    parsed_code = ast.parse(code_block)
    import_statements = []
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.Import):
            import_names = [
                f"import {name.name}"
                if name.asname is None
                else f"import {name.name} as {name.asname}"
                for name in node.names
            ]
            import_statements.extend(import_names)
        elif isinstance(node, ast.ImportFrom):
            module_name = (
                node.module
                if (node.module is not None and node.level == 0)
                else "." * node.level + (node.module or "")
            )
            import_names = [
                f"from {module_name} import {name.name}"
                if name.asname is None
                else f"from {module_name} import {name.name} as {name.asname}"
                for name in node.names
            ]
            import_statements.extend(import_names)

    import_block = "\n".join(["    " + statement for statement in import_statements])

    return import_block


def insert_string_after_colon(function_string: str, string_to_insert: str) -> str:
    pattern = r"def.*\(.*\).*:"
    match = re.search(pattern, function_string)
    if not match:
        return function_string

    pattern_index = match.end()
    return (
        function_string[:pattern_index]
        + "\n"
        + string_to_insert
        + function_string[pattern_index:]
    )


def check_and_install_libraries(import_statements: str) -> None:
    missing_libraries = []

    for line in import_statements.split("\n"):
        line = line.strip()
        if line.startswith("import"):
            statement = line.split(" ")[1]
        elif line.startswith("from"):
            statement = line.split(" ")[1].split(".")[0]
        else:
            continue

        try:
            importlib.import_module(statement)
        except ImportError:
            missing_libraries.append(statement)

    if missing_libraries:
        track.warning(f"Missing libraries: {', '.join(missing_libraries)}\n")
        install_libraries(missing_libraries)


def install_libraries(libraries: list) -> None:
    for library in libraries:
        track.warning(f"Installing library {library}\n")
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])

    track.warning(f"Libraries installed successfully\n")


def sampler(likelihood: float) -> bool:
    "Function that returns True or False depending on the likelihood provided. A higher likelihood indicates a bigger chances of returning True."
    random_number = random.random()
    track.warning(f"Random number: {random_number}, Likelihood: {likelihood}")

    if random_number < likelihood:
        return True
    else:
        return False


def rename_function(function_string: str, new_name: str) -> str:
    pattern = r"def\s+([a-zA-Z_]\w*)\s*\("
    match = re.search(pattern, function_string)

    if match:
        renamed_function = re.sub(pattern, f"def {new_name}(", function_string)
        return renamed_function
    else:
        track.warning(f"Could not rename function {function_string}")
        return function_string


def human_decision(prompt):
    while True:
        user_input = input(prompt).strip().lower()

        if user_input == "y":
            return True
        elif user_input == "n":
            return False
        else:
            track.error("Invalid input. Only 'y' for yes or 'n' for no vlaid.")
