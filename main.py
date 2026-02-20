import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
import sys
from prompts import system_prompt
from available_functions import available_functions


def main():
    if len(sys.argv) < 2 or sys.argv[1].strip() == "":
        print("Missing Value: Input prompt is required")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Set up the api key and client
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")
    client = genai.Client(api_key=api_key)

    # Generate content with the client
    model = "gemini-2.5-flash"

    try:
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, tools=[available_functions]
            ),
        )
        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print("Response:")
            print(response.text)
    except Exception as e:
        print(f"Failed model call on model: {model} with error {e}")


if __name__ == "__main__":
    main()
