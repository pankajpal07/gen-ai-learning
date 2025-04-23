from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL")
    )

def get_weather(city: str):
    print('get_weather: ', city)
    query = f'The response of https://wttr.in/{city}?format=%C+%t should contains the weather of that city'
    return request_gemini(query)

def run_command(command: str):
    print('run_command: ', command)
    result = os.system(command=command)
    return result

available_tools = {
    'get_weather': {
        'fn': get_weather,
        'description': 'Takes a city name as input and returns the current weather of that city'
    },
    'run_command': {
        'fn': run_command,
        'description': 'Takes a command to run in the user\'s system'
    }
}

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
    - if the output is finalized, then add a fun fact with the result to make it more interesting

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

    User Query: Make a directory in my system?
    Output: {'step': 'plan', 'content': 'The user wants to create a directory' }
    Output: {'step': 'plan', 'content': 'From the available tools, I should select run_command' }
    Output: {'step': 'action', 'function': 'run_command', 'input: 'mkdir filename' }
    Output: {'step': 'observe', 'output': 'filename' }
    Output: {'step': 'output', 'content': 'File is created with the name filename' }

    """

def request_gemini(user_query: str):

    messages = [
        { 'role': 'system', 'content': system_prompt },
        { 'role': 'user', 'content': user_query }
    ]

    while True:
        response = client.chat.completions.create(
            model=os.getenv('MODEL'),
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({'role': 'assistant', 'content': json.dumps(parsed_output)})

        if parsed_output.get('step') == 'plan':
            print(f'🧠:({parsed_output.get("step")})', parsed_output.get('content'))
            continue

        if parsed_output.get('step') == 'action':
            tool_name = parsed_output.get('function')
            tool_input = parsed_output.get('input')

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get('fn')(tool_input)
                messages.append({'role': 'assistant', 'content': json.dumps({'step': 'observe', 'output': output})})
                continue

        if parsed_output.get('step') == 'output':
            print('🤖:', parsed_output.get('content'))
            return parsed_output.get('content')


while True:
    query = input('> ')
    request_gemini(query)