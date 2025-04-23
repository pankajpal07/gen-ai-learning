from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "ooutput", "validate", and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next intput
3. Carefully analyse the user query

Output Format:
{{ step: "string", content: "string" }}

Example:
Input: What is 2 + 2
Output: {{ step: "analyse", content: "Alright! The user is interested in maths query and he is asking a basic arthematic oepration" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct answer for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}

"""

# message = input("🧓🏻: ")
# result = client.chat.completions.create(
#     model=os.getenv('MODEL'),
#     response_format={"type": "json_object"},
#     messages=[
#         {'role': 'system', 'content': system_prompt},
#         {'role': 'user', 'content': 'what is 3 + 4 * 5'},
#         {'role': 'assistant', 'content': json.dumps({"step": "analyse","content": "The user has provided an arithmetic expression: 3 + 4 * 5. This involves both addition and multiplication. I need to remember the order of operations."})},
#         {'role': 'assistant', 'content': json.dumps({"step": "think","content": "I need to follow the order of operations (PEMDAS/BODMAS). Multiplication comes before addition. So, I\'ll first multiply 4 and 5, and then add the result to 3."})},
#         {'role': 'assistant', 'content': json.dumps({"step": "output","content": "23"})},
#         {'role': 'assistant', 'content': json.dumps({"step": "validate","content": "4 * 5 = 20, and 3 + 20 = 23. The calculation seems correct."})},
#         {'role': 'assistant', 'content': json.dumps({"step": "result","content": "3 + 4 * 5 = 3 + 20 = 23. The multiplication is performed before addition according to the order of operations."})}
#     ]
# )

user_message = input("👨: ")
messages = [
    { "role": "system", "content": system_prompt },
    { "role": "user", "content": user_message }
]

while True:
    result = client.chat.completions.create(
        model=os.getenv('MODEL'),
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_response = json.loads(result.choices[0].message.content)
    messages.append({'role': 'assistant', 'content': json.dumps(parsed_response)})

    if parsed_response.get('step') != 'result':
        print("🧠: ", parsed_response.get('content'))
        continue

    print("🤖: ", parsed_response.get('content'))
    break


# result = client.chat.completions.create(
#     model=os.getenv('MODEL'),
#     response_format={"type": "json_object"},
#     messages=[
#         {'role': 'system', 'content': system_prompt},
#         {'role': 'user', 'content': 'what is 3 + 4 * 5'},
#         {'role': 'assistant', 'content': json.dumps({"step": "analyse","content": "The user has provided an arithmetic expression: 3 + 4 * 5. This involves both addition and multiplication. I need to remember the order of operations."})},
#         {'role': 'assistant', 'content': json.dumps({"step": "think","content": "I need to follow the order of operations (PEMDAS/BODMAS). Multiplication comes before addition. So, I\'ll first multiply 4 and 5, and then add the result to 3."})},
#         {'role': 'assistant', 'content': json.dumps({"step": "output","content": "23"})},
#         {'role': 'assistant', 'content': json.dumps({"step": "validate","content": "4 * 5 = 20, and 3 + 20 = 23. The calculation seems correct."})},
#         {'role': 'assistant', 'content': json.dumps({"step": "result","content": "3 + 4 * 5 = 3 + 20 = 23. The multiplication is performed before addition according to the order of operations."})}
#     ]
# )

print("🤖: ", result.choices[0].message.content)