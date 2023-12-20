__version__ = "0.0.12"

import copy
import functools
import traceback

from fukkatsu.llm.googlegate import reset_google_key, set_google_key
from fukkatsu.llm.openaigate import reset_openai_key, set_openai_key
from fukkatsu.memory import SHORT_TERM_MEMORY
from fukkatsu.observer.tracker import track
from fukkatsu.utils.helper import (check_and_install_libraries,
                                   extract_imports, extract_text_between_pipes,
                                   human_decision, insert_string_after_colon,
                                   remove_trace_lines, remove_wrapper_name,
                                   rename_function, return_input_arguments,
                                   return_source_code, sampler)
from fukkatsu.utils.synthesize import defibrillate, enhance, stalker, twin

set_openai_key()
set_google_key()


def resurrect(
    lives: int = 1,
    additional_req: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    primary_model_api: str = "openai",
    secondary_model_api: str = "openai",
    primary_config: dict = {},
    secondary_config: dict = {},
    human_action: bool = False,
    active_memory: bool = True,
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
                track.exception(e)
                trace = traceback.format_exc()
                trace = remove_trace_lines(trace)

                source = return_source_code(func)
                source = remove_wrapper_name(source)

                track.warning(f"Input arguments: {input_args}\n")
                track.warning(f"\nSource Code: \n {source}\n")

                if trace in SHORT_TERM_MEMORY.keys() and active_memory == True:
                    track.warning("Correction already in-memory\n")
                    suggested_code = SHORT_TERM_MEMORY[trace]
                    track.warning(
                        f"Using in-memory saved correction:\n{suggested_code}\n"
                    )

                else:
                    track.warning("Requesting INITIAL correction - Attempt 1\n")
                    suggested_code = defibrillate(
                        inputs=input_args,
                        faulty_function=source,
                        error_trace=trace,
                        model_api=primary_model_api,
                        config=primary_config,
                        additional_req=additional_req,
                    )
                    track.warning(
                        f"Received INITIAL RAW suggestion:\n{suggested_code}\n"
                    )
                    if active_twin == True:
                        track.warning("Requesting TWIN review\n")
                        suggested_code = twin(
                            inputs=input_args,
                            target_function=suggested_code,
                            model_api=secondary_model_api,
                            config=secondary_config,
                        )
                        track.warning(f"TWIN review complete:\n{suggested_code}")
                        suggested_code = rename_function(suggested_code, func.__name__)
                        track.warning(
                            f"Twin Safeguard: Function name changed to {suggested_code}\n"
                        )
                    suggested_code = extract_text_between_pipes(suggested_code)
                    track.warning(
                        f"Received INITIAL CLEANED suggestion:\n{suggested_code}\n"
                    )

                    import_block = extract_imports(suggested_code)
                    if allow_installs == True:
                        check_and_install_libraries(import_statements=import_block)

                    suggested_code = insert_string_after_colon(
                        suggested_code, import_block
                    )
                    track.warning(
                        f"Import block added to suggested code:\n {suggested_code}\n"
                    )

                for i in range(lives):

                    track.warning(f"Attempt {i+1} to reanimate\n")

                    try:
                        global_dict = globals()
                        local_dict = locals()

                        compiled_code = compile(suggested_code, "<string>", "exec")

                        exec(compiled_code, global_dict, local_dict)
                        new_function = local_dict[func.__name__]

                        locals()[func.__name__] = new_function

                        args_copy = copy.deepcopy(args)
                        kwargs_copy = copy.deepcopy(kwargs)

                        output = new_function(*args_copy, **kwargs_copy)

                        SHORT_TERM_MEMORY[trace] = suggested_code
                        track.warning(
                            f"Reanimation successful, using:\n{suggested_code}\n"
                        )
                        if human_action:
                            track.warning("Requesting human review\n")
                            decision = human_decision(
                                f"The following is the result of the reanimation attempt:\n{output}\nProceed? [y/n]"
                            )
                            if decision == True:
                                return output
                            else:
                                track.warning(
                                    "Human rejected correction. Terminating\n"
                                )
                                break
                        else:
                            return output

                    except Exception as e:
                        track.exception(e)

                        if i == lives - 1:
                            break

                        trace = traceback.format_exc()
                        trace = remove_trace_lines(trace)
                        track.warning("Reanimation failed, requesting new correction\n")

                        if trace in SHORT_TERM_MEMORY.keys() and active_memory == True:
                            track.warning("Correction already in-memory\n")
                            suggested_code = SHORT_TERM_MEMORY[trace]
                            track.warning(
                                f"Using in-memory saved correction:\n{suggested_code}\n"
                            )

                        else:
                            suggested_code = defibrillate(
                                inputs=input_args,
                                faulty_function=suggested_code,
                                error_trace=trace,
                                model_api=primary_model_api,
                                config=primary_config,
                                additional_req=additional_req,
                            )
                            track.warning(
                                f"Received attempt RAW suggestion:\n{suggested_code}\n"
                            )

                            if active_twin == True:
                                track.warning("Requesting TWIN review\n")
                                suggested_code = twin(
                                    inputs=input_args,
                                    target_function=suggested_code,
                                    model_api=secondary_model_api,
                                    config=secondary_config,
                                )
                                track.warning(
                                    f"TWIN review complete:\n{suggested_code}"
                                )
                                suggested_code = rename_function(
                                    suggested_code, func.__name__
                                )
                                track.warning(
                                    f"Twin Safeguard: Function name changed to {suggested_code}\n"
                                )

                            suggested_code = extract_text_between_pipes(suggested_code)
                            track.warning(
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
                            track.warning(
                                f"Import block added to suggested code:\n {suggested_code}\n"
                            )

                raise Exception(f"|__|__|______ {func.__name__} flatlined")

        return wrapper

    return _resurrect


def mutate(
    request: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    primary_model_api: str = "openai",
    secondary_model_api: str = "openai",
    primary_config: dict = {},
    secondary_config: dict = {},
    human_action: bool = False,
):
    def _mutate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            input_args = return_input_arguments(func, *args, **kwargs)
            source = return_source_code(func)
            source = remove_wrapper_name(source)

            track.warning(f"Input arguments: {input_args}\n")
            track.warning(f"\nSource Code: \n {source}\n")

            track.warning("Requesting mutation\n")
            suggested_code = enhance(
                inputs=input_args,
                target_function=source,
                model_api=primary_model_api,
                config=primary_config,
                request=request,
            )
            track.warning(f"Received RAW suggestion mutation:\n{suggested_code}\n")

            if active_twin == True:
                track.warning("Requesting TWIN review:\n")
                suggested_code = twin(
                    inputs=input_args,
                    target_function=suggested_code,
                    model_api=secondary_model_api,
                    config=secondary_config,
                )
                track.warning(f"TWIN review complete:\n{suggested_code}")
                suggested_code = rename_function(suggested_code, func.__name__)
                track.warning(
                    f"Twin Safeguard: Function name changed to {suggested_code}\n"
                )
                track.warning(f"TWIN review complete:\n{suggested_code}")
            suggested_code = extract_text_between_pipes(suggested_code)
            track.warning(f"Received CLEANED suggestion mutation: {suggested_code}\n")

            global_dict = globals()
            local_dict = locals()

            import_block = extract_imports(suggested_code)
            if allow_installs == True:
                check_and_install_libraries(import_statements=import_block)

            suggested_code = insert_string_after_colon(suggested_code, import_block)
            track.warning(f"Import block added to suggested code:\n {suggested_code}\n")

            compiled_code = compile(suggested_code, "<string>", "exec")

            exec(compiled_code, global_dict, local_dict)
            new_function = local_dict[func.__name__]

            locals()[func.__name__] = new_function

            output = new_function(*args, **kwargs)

            if human_action:
                track.warning("Requesting human review\n")
                decision = human_decision(
                    f"The following is the result of the mutation attempt:\n{output}\nProceed? [y/n]"
                )
                if decision == True:
                    track.warning(f"Human accepted mutation\n")
                    return output
                else:
                    raise Exception(f"Human rejected mutation. Terminating\n")

            track.warning(f"Mutation successful, using {suggested_code}\n")

            return output

        return wrapper

    return _mutate


def stalk(
    likelihood: float = 1.0,
    additional_req: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    primary_model_api: str = "openai",
    secondary_model_api: str = "openai",
    primary_config: dict = {},
    secondary_config: dict = {},
    human_action: bool = False,
):
    def _stalk(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            if sampler(likelihood) == False:
                track.warning(
                    "Continue without reviewing function, using original function\n"
                )
                return func(*args, **kwargs)

            input_args = return_input_arguments(func, *args, **kwargs)
            source = return_source_code(func)
            source = remove_wrapper_name(source)

            track.warning(f"Input arguments: {input_args}\n")
            track.warning(f"\nSource Code: \n {source}\n")

            track.warning("Stalking function\n")
            suggested_code = stalker(
                inputs=input_args,
                function=source,
                model_api=primary_model_api,
                config=primary_config,
                additional_req=additional_req,
            )
            track.warning(f"Received RAW suggestion from Stalker:\n{suggested_code}\n")

            if active_twin == True:
                track.warning("Requesting TWIN review:\n")
                suggested_code = twin(
                    inputs=input_args,
                    target_function=suggested_code,
                    model_api=secondary_model_api,
                    config=secondary_config,
                )
                track.warning(f"TWIN review complete:\n{suggested_code}")
                suggested_code = rename_function(suggested_code, func.__name__)
                track.warning(
                    f"Twin Safeguard: Function name changed to {suggested_code}\n"
                )

            suggested_code = extract_text_between_pipes(suggested_code)
            track.warning(f"Received CLEANED suggestion review: {suggested_code}\n")

            global_dict = globals()
            local_dict = locals()

            import_block = extract_imports(suggested_code)
            if allow_installs == True:
                check_and_install_libraries(import_statements=import_block)

            suggested_code = insert_string_after_colon(suggested_code, import_block)
            track.warning(f"Import block added to suggested code:\n {suggested_code}\n")

            compiled_code = compile(suggested_code, "<string>", "exec")

            exec(compiled_code, global_dict, local_dict)
            new_function = local_dict[func.__name__]

            locals()[func.__name__] = new_function

            output = new_function(*args, **kwargs)

            if human_action:
                track.warning("Requesting human review\n")
                decision = human_decision(
                    f"The following is the result of the correction attempt:\n{output}\nProceed? [y/n]"
                )
                if decision == True:
                    track.warning(f"Human accepted suggestion\n")
                    return output
                else:
                    raise Exception(f"Human rejected suggestion. Terminating\n")

            track.warning(f"Review successful, using {suggested_code}\n")

            return output

        return wrapper

    return _stalk
