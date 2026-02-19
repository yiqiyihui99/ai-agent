import os
import subprocess


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
