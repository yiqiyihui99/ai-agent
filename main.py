import os
import argparse
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
from prompts import system_prompt
from available_functions import available_functions
from functions.call_function import call_function


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant CLI")
    parser.add_argument(
        "user_prompt", nargs="+", help="The input prompt for gemini agent"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    user_prompt = " ".join(args.user_prompt)
    verbose = args.verbose
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")
    client = genai.Client(api_key=api_key)

    for _ in range(20):
        content, function_responses = generate_content(
            client, user_prompt, messages, verbose
        )
        if content.candidates:
            for candidate in content.candidates:
                messages.append(candidate.content)
        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))

        # Early finish should break the loop
        if not content.function_calls:
            print("Final response:")
            print(content.text)
            break

    if content.function_calls:
        print(f"No final response reached after 20 iterations")
        exit(1)


# Helper function to generate content using a model and call_function -> should output .parts and .function_response
def generate_content(client, user_prompt, messages, verbose):
    # Generate content with the client
    model = "gemini-2.5-flash"
    function_responses = []

    try:
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, tools=[available_functions]
            ),
        )
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=verbose)
                if not function_call_result.parts:
                    raise Exception("Function call result is empty")
                first_item = function_call_result.parts[0]
                if first_item.function_response == None:
                    raise Exception("Function response is None")

                function_responses.append(first_item)
                if verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )

    except Exception as e:
        print(f"Failed model call on model: {model} with error {e}")

    return response, function_responses


if __name__ == "__main__":
    main()
