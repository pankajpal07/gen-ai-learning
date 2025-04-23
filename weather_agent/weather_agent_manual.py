from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL")
    )

def get_weather(city: str):
    return "48 C"

system_prompt="""
You are a helpful AI agent who is psecialized in resolving user queries
You work on start, plan, action and observe mode
For the given user query and available tools, plan the step by step execution to resolve the query.
After proper planning, select the relevant tool from the available tool and based on the selected tool, you perform an action to call the tool.
Wait for the observations and based on the obseration from the tool called, resolve the user query

Rules:
 - Follow the strict JSON format.
 - Always perform one step at a time and wait for the input
 - carefully analyze the user query

Output:
{
    'step': 'string',
    'content': 'string',
    'function': 'The name of the function if and only if the step is action
    'input': 'The input paramter to the function
}

Available Tools:
 - get_weather

Example:
User Query: What is the temperature of Noida?
Output: {'step': 'plan', 'content': 'The user is asking the weather data of Noida' }
Output: {'step': 'plan', 'content': 'From the available tools, I should select get_weather' }
Output: {'step': 'action', 'function': 'get_weather', 'input: 'Noida' }
Output: {'step': 'observe', 'output': 'Temp. is 48' }
Output: {'step': 'output', 'content': 'The temp. of noida is 48' }

"""

response = client.chat.completions.create(
    model=os.getenv('MODEL'),
    response_format={"type": "json_object"},
    messages=[
        { 'role': 'system', 'content': system_prompt},
        { 'role': 'user', 'content': 'What is the temperate of Ghaziabad?'},
        # Manual addition
        { 'role': 'assistant', 'content': '{"step": "plan","content": "The user is asking for the temperature of Ghaziabad."}'},
        { 'role': 'assistant', 'content': '{"step": "plan","content": "I should use the \'get_weather\' tool to get the temperature of Ghaziabad.","function": null,"input": null}'},
        { 'role': 'assistant', 'content': '{"step": "action","content": "Call get_weather function","function": "get_weather","input": "Ghaziabad"}'},
        { 'role': 'assistant', 'content': '{"step": "observe","output": "The temperature in Ghaziabad is 47 degrees Celsius."}'},
        { 'role': 'assistant', 'content': '{"step": "output","content": "The temperature in Ghaziabad is 47 degrees Celsius."}'}
    ]
)

print(response.choices[0].message.content)