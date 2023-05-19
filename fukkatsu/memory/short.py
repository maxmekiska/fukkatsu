import json
import os

SHORT_TERM_MEMORY = {}


def save_memory() -> None:
    """Saves the current short term memory to a json file."""
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "memory.json")

    with open(file_path, "w") as json_file:
        json.dump(SHORT_TERM_MEMORY, json_file, indent=4, sort_keys=True)


def get_memory() -> dict:
    """Return current short term memory dictionary."""
    return SHORT_TERM_MEMORY
