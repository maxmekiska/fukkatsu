import fukkatsu
print(f"fukkatsu version running: {fukkatsu.__version__}")

from fukkatsu import resurrect

from datetime import datetime


@resurrect(
    lives=3,
    allow_installs = True,
    additional_req = "Ensure that all datestrings provided are transformed into datetime objects.",
    active_twin = True,
    primary_model_api = "google",
    secondary_model_api = "openai",
    primary_config = {"model": "gemini-pro", "temperature": 0.1},
    secondary_config = {"model": "gpt-3.5-turbo", "temperature": 0.1}, 
    human_action = True,
    active_memory = True
)
def perform_data_transformation(data):
    """takes in list of datestrings, transforms into datetime objects.
    """
    date_format = '%Y-%m-%d'
    
    for idx, date in enumerate(data):
        data[idx] = datetime.strptime(date, date_format)
        
    return data


data = [
        "2023-07-07", "1 June 2020",
        "2023.07.07", "2023-12-01",
        "2020/01/01", "Nov 11 1994"
        ]

transformed_data = perform_data_transformation(data)

print(transformed_data)
