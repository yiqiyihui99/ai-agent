import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    if not sys.argv[1] or sys.argv[1].strip() == "":
        print("Missing Value: Input prompt is required")
        sys.exit(1)
    
    user_prompt = sys.argv[1]
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
    model = "gemini-2.0-flash-001"
    response = client.models.generate_content(model=model, contents=messages)
    print(response.text)
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
