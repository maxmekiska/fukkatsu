import os

import openai

from fukkatsu.utils.prompt import (ADDITIONAL, CONTEXT, CONTEXT_MUTATE,
                                   OUTPUT_CONSTRAINTS,
                                   OUTPUT_CONSTRAINTS_MUTATE)

try:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    print("OPENAI_API_KEY found in environment variables.")
except:
    print("OPENAI_API_KEY not found in environment variables.")
    raise Exception("OPENAI_API_KEY not found in environment variables.")

MODEL = "gpt-3.5-turbo"


def defibrillate(
    inputs: str, faulty_function: str, error_trace: str, additional_req: str = ""
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

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": set_prompt},
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.1,
    )

    corrected_function = response["choices"][0]["message"]["content"].strip()

    return corrected_function


def enhance(inputs: str, target_function: str, request: str = "") -> str:
    set_prompt = (
        f"{CONTEXT_MUTATE}\n\n{target_function}\n\nThe function received the following inputs:\n\n"
        f"{inputs}\n\nThe user requests the following:\n{request}\n{OUTPUT_CONSTRAINTS_MUTATE}"
    )

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": set_prompt},
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.1,
    )

    mutated_function = response["choices"][0]["message"]["content"].strip()

    return mutated_function
