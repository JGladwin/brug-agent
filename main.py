import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def generate_content(client: genai.Client, messages: list[types.Content], available_functions: types.Tool, system_prompt: str) -> genai.types.GenerateContentResponse:
    return client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

def main():
    parser = argparse.ArgumentParser(description="Brug Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None or len(api_key) == 0:
        raise RuntimeError("Please set api key to run the application")
    client = genai.Client(api_key=api_key)
    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = generate_content(client, messages, available_functions, system_prompt)

    if not response.usage_metadata:
        raise RuntimeError("Cannot access data from Google's Gemimi APIs. Please check that access is available for given API key and it is not rate limited")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_calls: list[FunctionCall] | None = response.function_calls
    if function_calls is not None and len(function_calls) > 0:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
