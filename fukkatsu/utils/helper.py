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


def extract_text_between_backticks(message: str) -> str:
    start_idx = message.find("|||") + 3
    end_idx = message.rfind("|||")
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        return ""
    return message[start_idx:end_idx].strip()


def return_source_code(func: callable) -> str:
    source = inspect.getsource(func)
    return source


def return_input_arguments(func: callable, *args, **kwargs) -> dict:
    signature = inspect.signature(func)
    bound_args = signature.bind(*args, **kwargs)
    input_args = {k: bound_args.arguments[k] for k in signature.parameters.keys()}
    return input_args
