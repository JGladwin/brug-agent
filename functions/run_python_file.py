import os, subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
):
# ) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_file]
            if not (args is None or len(args) == 0):
                command.extend(args)
            process = subprocess.run(command, capture_output=True, text=True, timeout=30)
            return_code = process.returncode
            stdout = process.stdout
            stderr = process.stderr
            output = ""
            if return_code != 0:
                output += f"Process exited with code " + return_code + "\n"
            if len(stdout) + len(stderr) == 0:
                output += f"No output produced\n"
            output += "STDOUT:" + "\n" + stdout
            output += "STDERR:" + "\n" + stderr
            return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
