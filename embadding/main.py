from openai import OpenAI
import os
from dotenv import load_dotenv

def main():

    load_dotenv()

    api_key = os.getenv("API_KEY")

    client = OpenAI(
        api_key=api_key,
        base_url=os.getenv("BASE_URL")
    )

    text = "Eiffel Tower is in Paris and is a famous landmark, it is 324 meters tall"

    response = client.embeddings.create(
        model="text-embedding-004",
        input=text
    )

    print("Vector Embeddings : ", response.data[0].embedding)

if __name__ == "__main__":
    main()