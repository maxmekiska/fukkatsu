from typing import Union

from fukkatsu.llm.googlegate import (GoogleGenerateContentConfig,
                                     request_google_model)
from fukkatsu.llm.openaigate import (OpenaiChatCompletionConfig,
                                     request_openai_model)
from fukkatsu.observer.tracker import track
from fukkatsu.utils.prompt import (ADDITIONAL, CONTEXT, CONTEXT_MUTATE,
                                   CONTEXT_STALKER, CONTEXT_TWIN,
                                   OUTPUT_CONSTRAINTS,
                                   OUTPUT_CONSTRAINTS_MUTATE,
                                   OUTPUT_CONSTRAINTS_TWIN)

MODEL_API = {"openai": request_openai_model, "google": request_google_model}


def defibrillate(
    model_api: str,
    inputs: str,
    faulty_function: str,
    error_trace: str,
    additional_req: str = "",
    config: Union[OpenaiChatCompletionConfig, GoogleGenerateContentConfig] = None,
) -> str:
    if additional_req == "":
        set_prompt = (
            f"{CONTEXT}\n\n{faulty_function}\n\nThe function received the following inputs:\n\n"
            f"{inputs}\n\nAnd returned the following error trace:\n\n{error_trace}\n\n{OUTPUT_CONSTRAINTS}"
        )
    else:
        set_prompt = (
            f"{CONTEXT}\n\n{faulty_function}\n\nThe function received the following inputs:\n\n"
            f"{inputs}\n\nAnd returned the following error trace:\n\n{error_trace}\n\n{OUTPUT_CONSTRAINTS}\n"
            f"{ADDITIONAL}{additional_req}"
        )
    track.warning(f"API REQUEST to {model_api}")

    corrected_function = MODEL_API[model_api](set_prompt, **config)

    return corrected_function


def enhance(
    model_api: str,
    inputs: str,
    target_function: str,
    request: str = "",
    config: Union[OpenaiChatCompletionConfig, GoogleGenerateContentConfig] = None,
) -> str:
    set_prompt = (
        f"{CONTEXT_MUTATE}\n\n{target_function}\n\nThe function received the following inputs:\n\n"
        f"{inputs}\n\nThe user requests the following:\n{request}\n{OUTPUT_CONSTRAINTS_MUTATE}"
    )

    track.warning(f"API REQUEST to {model_api}")

    mutated_function = MODEL_API[model_api](set_prompt, **config)

    return mutated_function


def twin(
    model_api: str,
    inputs: str,
    target_function: str,
    config: Union[OpenaiChatCompletionConfig, GoogleGenerateContentConfig] = None,
) -> str:
    set_prompt = (
        f"{CONTEXT_TWIN}\n\n{target_function}\n\nThe function received the following inputs:\n\n"
        f"{inputs}\n\n{OUTPUT_CONSTRAINTS_TWIN}"
    )

    track.warning(f"API REQUEST to {model_api}")
    mutated_function = MODEL_API[model_api](set_prompt, **config)

    return mutated_function


def stalker(
    model_api: str,
    inputs: str,
    function: str,
    additional_req: str = "",
    config: Union[OpenaiChatCompletionConfig, GoogleGenerateContentConfig] = None,
) -> str:
    if additional_req == "":
        set_prompt = (
            f"{CONTEXT_STALKER}\n\n{function}\n\nThe function received the following inputs:\n\n"
            f"{inputs}\n\n{OUTPUT_CONSTRAINTS}\n"
        )
    else:
        set_prompt = (
            f"{CONTEXT}\n\n{function}\n\nThe function received the following inputs:\n\n"
            f"{inputs}\n\n{OUTPUT_CONSTRAINTS}\n"
            f"{ADDITIONAL}{additional_req}"
        )
    track.warning(f"API REQUEST to {model_api}")
    corrected_function = MODEL_API[model_api](set_prompt, **config)

    return corrected_function
