from openai import OpenAI
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    message = input("👨: ")
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL")
    )
    result = client.chat.completions.create(
        model=os.getenv('MODEL'),
        messages=[
            { "role": "user", "content": message}
        ]
    )

    print("🤖: ", result.choices[0].message.content)


if __name__ == "__main__":
    main()
