import os
from dataclasses import dataclass
from typing import Optional

import google.generativeai as genai

from fukkatsu.observer.tracker import track


@dataclass
class GoogleGenerateContentConfig:
    model: str
    candidate_count: Optional[int]
    stop_sequences: Optional[str]
    max_output_tokens: int
    temperature: float
    top_p: Optional[float]
    top_k: Optional[int]


def set_google_key():
    track.warning("Setting GOOGLE_API_KEY")
    try:
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        track.warning("GOOGLE_API_KEY found in environment variables.")
    except:
        track.error("GOOGLE_API_KEY not found in environment variables.")


def reset_google_key(key: str):
    if type(key) != str:
        track.error("Invalid Key format. GOOGLE_API_KEY not overwritten.")
        raise Exception("Invalid Key format. GOOGLE_API_KEY not overwritten.")
    else:
        genai.configure(api_key=key)
        track.warning("GOOGLE_API_KEY overwritten.")


def request_google_model(
    set_prompt: str,
    model: str = "gemini-pro",
    candidate_count: Optional[int] = 1,
    stop_sequences: str = None,
    max_output_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
):

    track.warning(
        f"API REQUEST to {model} - Temperature: {temperature} - Max Tokens: {max_output_tokens} - candidate_count: {candidate_count} - Stop: {stop_sequences}"
    )
    model = genai.GenerativeModel(model)
    response = model.generate_content(
        set_prompt,
        generation_config=genai.types.GenerationConfig(
            candidate_count=candidate_count,
            stop_sequences=stop_sequences,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        ),
    )

    final_resoponse = response.text

    return final_resoponse
