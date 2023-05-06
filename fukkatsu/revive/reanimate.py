import functools
import logging
import traceback

from fukkatsu.memory import SHORT_TERM_MEMORY
from fukkatsu.utils import (extract_text_between_backticks, remove_trace_lines,
                            remove_wrapper_name, return_input_arguments,
                            return_source_code)
from fukkatsu.utils.medic import defibrillate


def resurrect(lives=1):
    def _resurrect(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            try:
                result = func(*args, **kwargs)
                return result

            except Exception as e:
                logging.exception(e)
                trace = traceback.format_exc()
                trace = remove_trace_lines(trace)

                input_args = return_input_arguments(func, *args, **kwargs)
                source = return_source_code(func)
                source = remove_wrapper_name(source)

                logging.warning(f"Input arguments: {input_args}")
                logging.warning(f"\nSource Code: \n {source}")

                if trace in SHORT_TERM_MEMORY.keys():
                    logging.warning("Correction already in memory")
                    suggested_code = SHORT_TERM_MEMORY[trace]

                else:
                    logging.warning("Requesting correction")
                    suggested_code = defibrillate(
                        inputs=input_args, faulty_function=source, error_trace=trace
                    )
                    suggested_code = extract_text_between_backticks(suggested_code)

                for i in range(lives):
                    logging.warning(f"Attempt {i+1} to reanimate")

                    try:
                        global_dict = globals().copy()
                        local_dict = locals().copy()

                        compiled_code = compile(suggested_code, "<string>", "exec")

                        exec(compiled_code, global_dict, local_dict)
                        new_function = local_dict[func.__name__]

                        SHORT_TERM_MEMORY[trace] = suggested_code
                        logging.warning(
                            f"Reanimation successful, using {suggested_code}"
                        )

                        return new_function(*args, **kwargs)
                    except:
                        logging.exception(e)
                        trace = traceback.format_exc()
                        trace = remove_trace_lines(trace)
                        logging.warning("Reanimation failed, requesting new correction")

                        if trace in SHORT_TERM_MEMORY.keys():
                            logging.warning("Correction already in memory")
                            suggested_code = SHORT_TERM_MEMORY[trace]
                            logging.warning(f"using {suggested_code}")

                        else:
                            suggested_code = defibrillate(
                                inputs=input_args,
                                faulty_function=suggested_code,
                                error_trace=trace,
                            )

                raise Exception(f"|__|__|______ {func.__name__} flatlined")

        return wrapper

    return _resurrect
