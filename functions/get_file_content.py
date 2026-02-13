import os
from config import MAX_FILE_READ_CHARS


def get_file_content(working_directory, file_path):

    content = ""

    combined_path = os.path.join(working_directory, file_path)
    target_file = os.path.abspath(os.path.normpath(combined_path))
    working_dir_abs = os.path.abspath(working_directory)  # abs ref req for .commonpath
    valid_target_file = (
        os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    )
    if not valid_target_file:
        content += f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        return content
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as file:
            file_contents = file.read(MAX_FILE_READ_CHARS)
            content += file_contents
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARS} characters]'
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

    return content
