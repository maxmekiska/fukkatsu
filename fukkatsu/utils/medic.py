import os

import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

MODEL = "gpt-3.5-turbo"


CONTEXT = """Repair and improve the following faulty function: """


def defibrillate(inputs: str, faulty_function: str, error_trace: str) -> str:
    prompt = f"{CONTEXT}\n\n{faulty_function}\n\nThe function received the following inputs:\n\n{inputs}\n\nAnd returned the following error trace:\n\n{error_trace}\n\nRespond with exactly one code box. Provide only the code of the corrected function. Do not use any additional libraries. Do not provide examples."

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt},
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.1,
    )

    corrected_function = response["choices"][0]["message"]["content"].strip()

    return corrected_function
