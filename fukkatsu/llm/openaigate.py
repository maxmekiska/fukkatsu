import os

import openai

from fukkatsu.observer.tracker import track


def set_openai_key():
    track.warning("Setting OPENAI_API_KEY")
    try:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        track.warning("OPENAI_API_KEY found in environment variables.")
    except:
        track.error("OPENAI_API_KEY not found in environment variables.")


def reset_openai_key(key: str):
    if type(key) != str:
        track.error("Invalid Key format. OPENAI_API_KEY not overwritten.")
        raise Exception("Invalid Key format. OPENAI_API_KEY not overwritten.")
    else:
        openai.api_key = key
        track.warning("OPENAI_API_KEY overwritten.")


def request_openai_model(
    set_prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.1,
    max_tokens: int = 1024,
    n: int = 1,
    stop: str = None,
):

    track.warning(
        f"API REQUEST to {model} - Temperature: {temperature} - Max Tokens: {max_tokens} - N: {n} - Stop: {stop}"
    )
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": set_prompt},
        ],
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
    )

    final_resoponse = response["choices"][0]["message"]["content"].strip()

    return final_resoponse
