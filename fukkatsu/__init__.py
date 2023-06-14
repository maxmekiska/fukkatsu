__version__ = "0.0.5"

import copy
import functools
import logging
import traceback

from fukkatsu.memory import SHORT_TERM_MEMORY
from fukkatsu.utils import (check_and_install_libraries, extract_imports,
                            extract_text_between_pipes,
                            insert_string_after_colon, remove_trace_lines,
                            remove_wrapper_name, return_input_arguments,
                            return_source_code)
from fukkatsu.utils.medic import defibrillate, enhance, twin


def resurrect(
    lives: int = 1,
    additional_req: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    llm: dict = {"primary": "gpt-3.5-turbo", "secondary": "gpt-3.5-turbo"},
    temperature: dict = {"primary": 0.1, "secondary": 0.1},
):
    def _resurrect(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            input_args = return_input_arguments(func, *args, **kwargs)

            try:
                args_copy = copy.deepcopy(args)
                kwargs_copy = copy.deepcopy(kwargs)
                result = func(*args_copy, **kwargs_copy)

                return result

            except Exception as e:
                logging.exception(e)
                trace = traceback.format_exc()
                trace = remove_trace_lines(trace)

                source = return_source_code(func)
                source = remove_wrapper_name(source)

                logging.warning(f"Input arguments: {input_args}\n")
                logging.warning(f"\nSource Code: \n {source}\n")

                if trace in SHORT_TERM_MEMORY.keys():
                    logging.warning("Correction already in-memory\n")
                    suggested_code = SHORT_TERM_MEMORY[trace]
                    logging.warning(
                        f"Using in-memory saved correction:\n{suggested_code}\n"
                    )

                else:
                    logging.warning("Requesting INITIAL correction\n")
                    suggested_code = defibrillate(
                        inputs=input_args,
                        faulty_function=source,
                        error_trace=trace,
                        model=llm["primary"],
                        temperature=temperature["primary"],
                        additional_req=additional_req,
                    )
                    logging.warning(
                        f"Received INITIAL RAW suggestion:\n{suggested_code}\n"
                    )
                    if active_twin == True:
                        logging.warning("Requesting TWIN review\n")
                        suggested_code = twin(
                            inputs=input_args,
                            target_function=suggested_code,
                            model=llm["secondary"],
                            temperature=temperature["secondary"],
                        )
                        logging.warning(f"TWIN review complete:\n{suggested_code}")
                    suggested_code = extract_text_between_pipes(suggested_code)
                    logging.warning(
                        f"Received INITIAL CLEANED suggestion:\n{suggested_code}\n"
                    )

                    import_block = extract_imports(suggested_code)
                    if allow_installs == True:
                        check_and_install_libraries(import_statements=import_block)

                    suggested_code = insert_string_after_colon(
                        suggested_code, import_block
                    )
                    logging.warning(
                        f"Import block added to suggested code:\n {suggested_code}\n"
                    )

                for i in range(lives):
                    logging.warning(f"Attempt {i+1} to reanimate\n")

                    try:
                        global_dict = globals()
                        local_dict = locals()

                        compiled_code = compile(suggested_code, "<string>", "exec")

                        exec(compiled_code, global_dict, local_dict)
                        new_function = local_dict[func.__name__]

                        SHORT_TERM_MEMORY[trace] = suggested_code
                        logging.warning(
                            f"Reanimation successful, using:\n{suggested_code}\n"
                        )
                        locals()[func.__name__] = new_function

                        args_copy = copy.deepcopy(args)
                        kwargs_copy = copy.deepcopy(kwargs)

                        return new_function(*args_copy, **kwargs_copy)

                    except:
                        logging.exception(e)
                        trace = traceback.format_exc()
                        trace = remove_trace_lines(trace)
                        logging.warning(
                            "Reanimation failed, requesting new correction\n"
                        )

                        if trace in SHORT_TERM_MEMORY.keys():
                            logging.warning("Correction already in-memory\n")
                            suggested_code = SHORT_TERM_MEMORY[trace]
                            logging.warning(
                                f"Using in-memory saved correction:\n{suggested_code}\n"
                            )

                        else:
                            suggested_code = defibrillate(
                                inputs=input_args,
                                faulty_function=suggested_code,
                                error_trace=trace,
                                model=llm["primary"],
                                temperature=temperature["primary"],
                                additional_req=additional_req,
                            )
                            logging.warning(
                                f"Received attempt RAW suggestion:\n{suggested_code}\n"
                            )

                            if active_twin == True:
                                logging.warning("Requesting TWIN review\n")
                                suggested_code = twin(
                                    inputs=input_args,
                                    target_function=suggested_code,
                                    model=llm["secondary"],
                                    temperature=temperature["secondary"],
                                )
                                logging.warning(
                                    f"TWIN review complete:\n{suggested_code}"
                                )
                            suggested_code = extract_text_between_pipes(suggested_code)
                            logging.warning(
                                f"Received attempt CLEANED suggestion:\n{suggested_code}\n"
                            )

                            import_block = extract_imports(suggested_code)
                            if allow_installs == True:
                                check_and_install_libraries(
                                    import_statements=import_block
                                )

                            suggested_code = insert_string_after_colon(
                                suggested_code, import_block
                            )
                            logging.warning(
                                f"Import block added to suggested code:\n {suggested_code}\n"
                            )

                raise Exception(f"|__|__|______ {func.__name__} flatlined")

        return wrapper

    return _resurrect


def mutate(
    request: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    llm: dict = {"primary": "gpt-3.5-turbo", "secondary": "gpt-3.5-turbo"},
    temperature: dict = {"primary": 0.1, "secondary": 0.1},
):
    def _mutate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            input_args = return_input_arguments(func, *args, **kwargs)
            source = return_source_code(func)
            source = remove_wrapper_name(source)

            logging.warning(f"Input arguments: {input_args}\n")
            logging.warning(f"\nSource Code: \n {source}\n")

            logging.warning("Requesting mutation\n")
            suggested_code = enhance(
                inputs=input_args,
                target_function=source,
                model=llm["primary"],
                temperature=temperature["primary"],
                request=request,
            )
            logging.warning(f"Received RAW suggestion mutation:\n{suggested_code}\n")

            if active_twin == True:
                logging.warning("Requesting TWIN review:\n")
                suggested_code = twin(
                    inputs=input_args,
                    target_function=suggested_code,
                    model=llm["secondary"],
                    temperature=temperature["secondary"],
                )
                logging.warning(f"TWIN review complete:\n{suggested_code}")
            suggested_code = extract_text_between_pipes(suggested_code)
            logging.warning(f"Received CLEANED suggestion mutation: {suggested_code}\n")

            global_dict = globals()
            local_dict = locals()

            import_block = extract_imports(suggested_code)
            if allow_installs == True:
                check_and_install_libraries(import_statements=import_block)

            suggested_code = insert_string_after_colon(suggested_code, import_block)
            logging.warning(
                f"Import block added to suggested code:\n {suggested_code}\n"
            )

            compiled_code = compile(suggested_code, "<string>", "exec")

            exec(compiled_code, global_dict, local_dict)
            new_function = local_dict[func.__name__]

            logging.warning(f"Mutation successful, using {suggested_code}\n")
            locals()[func.__name__] = new_function

            return new_function(*args, **kwargs)

        return wrapper

    return _mutate
