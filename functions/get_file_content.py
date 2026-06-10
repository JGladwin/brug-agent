import os.path
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content (at most {MAX_CHARS} characters) from the required file present relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read file from, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            # We don't want to accidentally read a gigantic file and send all that data to the LLM... to avoid burning through our token limits.
            with open(target_file) as f:
                content = f.read(MAX_CHARS)
                if f.read(1):
                    content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f'Error: {e}'
