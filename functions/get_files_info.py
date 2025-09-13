import os


def get_files_info(working_directory, directory="."):
    if directory == ".":
        header = "Result for current directory:\n"
    else:
        header = f"Result for '{directory}' directory:\n"
    files_info = header
    new_path = os.path.join(working_directory, directory)  
    if not os.path.abspath(new_path).startswith(os.path.abspath(working_directory)):
        files_info += f'    Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        return files_info
    if not os.path.isdir(new_path):
        files_info += f'    Error: "{directory}" is not a directory\n'
        return files_info
    try:
        for file in os.listdir(new_path):
                file_path = os.path.join(new_path, file)
                # output file info
                name = file,
                file_size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                out = f" - {file}: file_size={file_size} bytes, is_dir={is_dir}"
                files_info += out + "\n"
    except Exception as e:
        files_info += f"    Error: {e}\n"
    return files_info