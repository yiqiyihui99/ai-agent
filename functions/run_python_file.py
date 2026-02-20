import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    combined_path = os.path.join(working_directory, file_path)
    target_file = os.path.abspath(os.path.normpath(combined_path))
    working_dir_abs = os.path.abspath(working_directory)  # abs ref req for .commonpath
    valid_target_file = (
        os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    )
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args:
        command.extend(args)
    try:
        completed_subprocess = subprocess.run(
            command, cwd=working_dir_abs, text=True, capture_output=True, timeout=30
        )

        output_str_array = []

        if completed_subprocess.returncode != 0:
            output_str_array.append(f"Process exited with code {completed_subprocess.returncode}")
        if not completed_subprocess.stdout and not completed_subprocess.stderr:
            output_str_array.append(f"No output produced")
        else:
            if completed_subprocess.stdout:
                output_str_array.append(f"STDOUT:\n{completed_subprocess.stdout}")
            if completed_subprocess.stderr:
                output_str_array.append(f"STDERR:\n{completed_subprocess.stderr}")
    except Exception as e:
        return f"Error: executing Python file: {e}"

    return "\n".join(output_str_array)

# TODO: ADD SCEHMA FOR RUN_PYTHON_FILE, WRITE_FILE
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file in a specified directory givvn the working directory, file path, and optional arguments",
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
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass to the python file if needed by a function",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
