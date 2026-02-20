import os
from config import MAX_FILE_READ_CHARS
from google.genai import types


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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists file content from a file in a specified directory relative to the working directory, providing the file info",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path of the working directory that we read target file from",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read from the working directory relative to the working directory path (working_directory)",
            ),
        },
    ),
)
