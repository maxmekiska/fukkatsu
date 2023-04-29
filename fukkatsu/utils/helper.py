import inspect
import re


def remove_trace_lines(trace_error: str) -> str:
    pattern = r"\b\w*line\s\d+\w*\b"
    output_str = re.sub(pattern, "", trace_error)
    return output_str


def remove_wrapper_name(source_code: str) -> str:
    start_index = source_code.index("def")
    source_code = source_code[start_index:]
    return source_code


def return_source_code(func: callable) -> str:
    source = inspect.getsource(func)
    return source


def return_input_arguments(func: callable, *args, **kwargs) -> dict:
    signature = inspect.signature(func)
    bound_args = signature.bind(*args, **kwargs)
    input_args = {k: bound_args.arguments[k] for k in signature.parameters.keys()}
    return input_args
