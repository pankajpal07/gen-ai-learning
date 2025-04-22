from dotenv import load_dotenv
from openai import OpenAI
import os

def main():

    load_dotenv()
    message = input("What you want to ask Gemini?\n")
    client = OpenAI()
    result = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            { "role": "user", "content": message}
        ]
    )

    print("Response: ", result.choices[0].message.content)

if __name__ == "__main__":
    main()
