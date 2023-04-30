import os
import openai


openai.api_key = os.environ.get("API_KEY") 
model_temp = os.environ.get("MODEL_TEMP")
MODEL = "code-davinci-002"


CONTEXT = """Repair and improve the following function: """


def request_correction(inputs: str, faulty_function: str, error_trace: str) -> str:
    prompt = f"{CONTEXT}\n\n{faulty_function}\n\nThe function received the following inputs:\n\n{inputs}\n\nAnd returned the following error trace:\n\n{error_trace}"

    model_engine = MODEL

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=model_temp,
    )

    corrected_function = response.choices[0].text.strip()

    return corrected_function
