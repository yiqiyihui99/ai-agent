import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    """
    Gets metadata for current/subdirectory's items, making sure to guard access for out of bounds items/directories
    """
    if directory == ".":
        header = "Result for current directory:\n"
    else:
        header = f"Result for '{directory}' directory:\n"
    files_info = header
    combined_path = os.path.join(working_directory, directory)
    target_dir = os.path.abspath(os.path.normpath(combined_path))
    working_dir_abs = os.path.abspath(working_directory)  # abs ref req for .commonpath
    valid_target_dir = (
        os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    )

    if not valid_target_dir:
        files_info += f'    Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        return files_info
    if not os.path.isdir(target_dir):
        files_info += f'    Error: "{directory}" is not a directory\n'
        return files_info
    try:
        for file in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file)
            # output file info
            name = (file,)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            out = f" - {file}: file_size={file_size} bytes, is_dir={is_dir}"
            files_info += out + "\n"
    except Exception as e:
        files_info += f"    Error: {e}\n"
    return files_info


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
