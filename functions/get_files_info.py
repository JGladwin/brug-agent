import os
from google.genai import types

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

def get_files_info(working_directory: str, directory: str = ".") -> str:
    #Directory parameter will be treated as a relative path within the working_directory. We allow the LLM agent to specify which directory it wants to scan, but the working_directory will be set by us. This means we can limit the scope of directories and files that the LLM is able to view.
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            #return f'Success: "{directory}" is within the working directory')
            target_dir_list = os.listdir(target_dir)
            data = "\n".join(map(
                lambda fs_item: f"- {fs_item}: file_size={os.path.getsize(os.path.join(target_dir, fs_item))}, is_dir={os.path.isdir(os.path.join(target_dir, fs_item))}", 
                target_dir_list
                ))
            return data
    except Exception as e:
        return f'Error: {e}'
