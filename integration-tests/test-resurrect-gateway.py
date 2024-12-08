import fukkatsu
print(f"fukkatsu version running: {fukkatsu.__version__}")

from fukkatsu import resurrect

from datetime import datetime


@resurrect(
    lives=3,
    allow_installs = True,
    additional_req = "Ensure that all datestrings provided are transformed into datetime objects.",
    active_twin = False,
    primary_model_api = "gateway",
    secondary_model_api="gateway",
    primary_config = {"temperature": 0.01, "model": "meta-llama/llama-3.1-8b-instruct:free"},
    secondary_config= {"temperature": 0.3 },
    human_action = False,
    active_memory = True
)
def perform_data_transformation(data):
    """takes in list of datestrings, transforms into datetime objects.
    """
    date_format = '%Y-%m-%d'

    for idx, date in enumerate(data):
        data[idx] = datetime.strptime(date, date_format)

    return data

if __name__ == "__main__":

    data = [
            "2023-07-07", "1 June 2020",
            "2023.07.07", "2023-12-01",
            "2020/01/01", "Nov 11 1994"
            ]

    transformed_data = perform_data_transformation(data)
    print(transformed_data)
