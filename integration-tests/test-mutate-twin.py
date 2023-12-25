import fukkatsu
print(f"fukkatsu version running: {fukkatsu.__version__}")

from fukkatsu import mutate

import pandas as pd

file_path = "status_field_v2.csv"

@mutate(request="look at the input file, make sure to change the function according to the file.",
        active_twin = True,
        primary_model_api = "google",
        primary_config= {"model": "gemini-pro", "temperature": 0.2},
        secondary_model_api = "openai",
        secondary_config = {"model": "gpt-3.5-turbo", "temperature": 0.2} 
        )
def read_file(file_path: str):
    """read file and return a data frame"""
    df = pd.read_excel(file_path)
    return df

print(read_file(file_path))