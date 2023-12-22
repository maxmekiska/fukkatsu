from typing import Optional

import openai

from fukkatsu.observer.tracker import track


def request_openai_model(
    set_prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.1,
    max_tokens: int = 1024,
    n: int = 1,
    stop: Optional[str] = None,
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
