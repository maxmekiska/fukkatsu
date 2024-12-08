import fukkatsu
print(f"fukkatsu version running: {fukkatsu.__version__}")

from fukkatsu import mutate

import pandas as pd

file_path = "status_field_v2.csv"

@mutate(request="look at the input file, make sure to change the function according to the file.",
        active_twin = True,
        primary_model_api = "gateway",
        primary_config = {"temperature": 0.01, "model": "meta-llama/llama-3.1-8b-instruct:free"},
        secondary_model_api = "gateway",
        secondary_config= {"temperature": 0.2, "model": "meta-llama/llama-3.1-8b-instruct:free"},
        )
def read_file(file_path: str):
    """read file and return a data frame"""
    df = pd.read_excel(file_path)
    return df

print(read_file(file_path))
