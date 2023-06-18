import os

import openai

from fukkatsu.observer.tracker import track
from fukkatsu.utils.prompt import (ADDITIONAL, CONTEXT, CONTEXT_MUTATE,
                                   CONTEXT_TWIN, OUTPUT_CONSTRAINTS,
                                   OUTPUT_CONSTRAINTS_MUTATE,
                                   OUTPUT_CONSTRAINTS_TWIN)

try:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    print("OPENAI_API_KEY found in environment variables.")
except:
    print("OPENAI_API_KEY not found in environment variables.")
    raise Exception("OPENAI_API_KEY not found in environment variables.")


def defibrillate(
    inputs: str,
    faulty_function: str,
    error_trace: str,
    model: str,
    temperature: float,
    additional_req: str = "",
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
    track.warning(f"API REQUEST to {model}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": set_prompt},
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temperature,
    )

    corrected_function = response["choices"][0]["message"]["content"].strip()

    return corrected_function


def enhance(
    inputs: str, target_function: str, model: str, temperature: float, request: str = ""
) -> str:
    set_prompt = (
        f"{CONTEXT_MUTATE}\n\n{target_function}\n\nThe function received the following inputs:\n\n"
        f"{inputs}\n\nThe user requests the following:\n{request}\n{OUTPUT_CONSTRAINTS_MUTATE}"
    )

    track.warning(f"API REQUEST to {model}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": set_prompt},
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temperature,
    )

    mutated_function = response["choices"][0]["message"]["content"].strip()

    return mutated_function


def twin(
    inputs: str,
    target_function: str,
    model: str,
    temperature: float,
) -> str:
    set_prompt = (
        f"{CONTEXT_TWIN}\n\n{target_function}\n\nThe function received the following inputs:\n\n"
        f"{inputs}\n\n{OUTPUT_CONSTRAINTS_TWIN}"
    )

    track.warning(f"API REQUEST to {model}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": set_prompt},
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temperature,
    )

    mutated_function = response["choices"][0]["message"]["content"].strip()

    return mutated_function
