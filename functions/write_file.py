import os
from google.genai import types


def write_file(working_directory, file_path, content):
    combined_path = os.path.join(working_directory, file_path)
    target_file = os.path.abspath(os.path.normpath(combined_path))
    working_dir_abs = os.path.abspath(working_directory)  # abs ref req for .commonpath
    valid_target_file = (
        os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    )

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    # create parent directory if it doesn't exist
    parent_dir = os.path.dirname(file_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    try:
        with open(target_file, "w") as file:
            file.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to or overwrites a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path of the working directory that we write to the target file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write to the working directory relative to the working directory path (working_directory)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file, or overwrite the file with if it already exists",
            ),
        },
    ),
)
