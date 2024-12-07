from typing import Optional

from openai import OpenAI

from fukkatsu.observer.tracker import track


def request_model(
    set_prompt: str,
    model: str = "meta-llama/llama-3.2-3b-instruct:free",
    base_url: str = "https://openrouter.ai/api/v1",
    temperature: float = 0.1,
    max_tokens: int = 1024,
    n: int = 1,
    stop: Optional[str] = None,
):
    client = OpenAI(
        base_url=base_url,
    )

    track.warning(
        f"API REQUEST to {model} - Temperature: {temperature} - Max Tokens: {max_tokens} - N: {n} - Stop: {stop}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": set_prompt},
        ],
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
    )

    track.warning(response)

    if response.choices[0].message.content:
        final_resoponse = response.choices[0].message.content.strip()
    else:
        response.choices[0].message.content

    return final_resoponse
