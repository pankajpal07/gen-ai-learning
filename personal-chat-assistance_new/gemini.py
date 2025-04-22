from openai import OpenAI
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    message = input("👨: ")
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    result = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            { "role": "user", "content": message}
        ]
    )

    print("🤖: ", result.choices[0].message.content)


if __name__ == "__main__":
    main()
