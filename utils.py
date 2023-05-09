import os
from constants import SCRIPTS_PATH

CWD_PATH = os.getcwd()


class ValidationError(Exception):
    """
    Script was marked by the model as invalid
    """
    def __init__(self, user_prompt: str):
        self.msg = f"PROMPT: {user_prompt}\nThe model failed to generate a valid script\n"

    def __str__(self) -> str:
        return self.msg


def save_script(script: str):
    """
    Save the generated Node.js script to the file system.

    This function saves the generated Node.js script to the file system in the directory specified by the `SCRIPTS_PATH`
    constant. The saved script filename follows the naming convention `script_<index>.js`, where `<index>` is an integer
    larger than any previously saved script.

    :param script: The Node.js script to be saved.
    :return: The index of the saved script.
    """
    # Create the `save to` directory if it does not exist
    save_to_path = os.path.join(CWD_PATH, SCRIPTS_PATH)
    if not os.path.isdir(save_to_path):
        os.makedirs(save_to_path)

    # Get a list of all the files in the directory that match the naming convention
    files = [
        f for f in os.listdir(save_to_path) if f.startswith("script_") and f.endswith(".js")
    ]

    # Extract the index from each filename and find the maximum value
    indices = [int(f.lstrip("script_").rstrip('.js')) for f in files]
    max_index = max(indices) if indices else 0

    # Generate a new filename using the maximum index + 1
    new_file_name = f"script_{max_index + 1}.js"

    # Save the script
    with open(os.path.join(save_to_path, new_file_name), "w") as file:
        file.write(script)
        file.write("\nconst args = process.argv.slice(2)\ntest(...args)")

    return str(max_index + 1)
