import os, sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import call_function, available_functions
from config import MAX_ITERS

def generate_content(client: genai.Client, messages: list[types.Content], available_functions: types.Tool, system_prompt: str, verbose: bool) -> str | None:
    response = client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    if not response.usage_metadata:
        raise RuntimeError("Cannot access data from Google's Gemimi APIs. Please check that access is available for given API key and it is not rate limited")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates is not None:
        for candidate in response.candidates:
            messages.append(candidate.content)

    function_calls: list[FunctionCall] | None = response.function_calls
    if function_calls is not None and len(function_calls) > 0:
        function_results: list[types.Part] = []
        for function_call in function_calls:
            function_call_result:types.Content = call_function(function_call, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or not function_call_result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function_call.name}")
            else:
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_results.append(function_call_result.parts[0])
        messages.append(types.Content(role="user", parts=function_results))
    else:
        return response.text

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
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, available_functions, system_prompt, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
