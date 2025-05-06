# Automation
import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
import time

load_dotenv()

client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL")
    )

def run_command_and_read_output(command: str):
    print("🔨 Tool Called: run_command_and_read_output", command)
    # execute command
    # return result
    # result = os.system(command=command)
    result = subprocess.check_output(command, shell=True)
    print("🔨 (out)", result.decode('utf-8'))
    return result.decode('utf-8')

def run_command(command):
    print("🔨 Tool Called: run_command", command)
    # execute command
    # return result
    result = os.system(command=command)

    return result

def read_file(file_path):
    print("🔨 Tool Called: read_file", file_path)
    # read file
    # return content
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def get_weather(city: str):
    # TODO: Perform an actual API call
    print("🔨 Tool Called: get_weather", city)

    url = f"https://wttr.in/{city}?format=%C+%t"

    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather of that city.",
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on sustem and should be called when the output doesn't matters.",
    },
    "run_command_and_read_output": {
        "fn": run_command_and_read_output,
        "description": "Takes a command as input to execute on sustem and return the command output. This should be called when you wants to read the output of the command.",
    },
    "read_file": {
        "fn": read_file,
        "description": "Takes a file path as input and returns the content of the file.",
    }
}

system_prompt = f"""
    You are an helpful AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe, error and output mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool
    Wait for the observation and based on the observation from the tool call resolve the user query.
    If you feel that in any prompt, there is a code error then you have to fix that code error and then run the complete process again from start, plan, action, observe and this time you have to give the correct output with more relevant prompt.
    If you want you can also update the system prompt to make it more relevant and useful for the user when it comes next time, but system_prompt is genetic, don't change it too much for a single user or query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next intput 
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather of that city.
    - run_command: Takes a command as input to execute on system.
    - read_file: Takes a file path as input and returns the content of the file.
    - run_command_and_read_output: Takes a command as input to execute on system and return the command output.

    Example:
    User Query:  What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Celcius" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

    User Query:  What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "error", "output": "some error occured when fethcing weather" }}
    Output: {{ "step": "plan", "output": "Ok, there was some error, now I have to fix the error and run the process again" }}
    Output: {{ "step": "plan", "output": "The error is in the tool to need to update the tool" }}
    Output: {{ "step": "action", "function": "run_command", "input": "command to update the code" }}
    Output: {{ "step": "observe", "content": "Now, I think the issue has been fixed, let's try the process again" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Celcius" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""

messages = [
    { 'role': 'system', 'content': system_prompt },
]

while True:
    user_query = input('> ')

    messages.append({ 'role': 'user', 'content': user_query })

    while True:
        try:
            response = client.chat.completions.create(
                model=os.getenv('MODEL'),
                response_format={"type": "json_object"},
                messages=messages,
            )
        except:
            time.sleep(30)
            continue

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({ 'role': 'assistant', 'content': json.dumps(parsed_output) })

        if parsed_output['step'] == 'plan':
            print(f"🧠: {parsed_output.get('content')}")
            continue
        
        if parsed_output['step'] == 'action':
            tool_name = parsed_output.get('function')
            tool_input = parsed_output.get('input')

            if available_tools.get(tool_name, False) != False:
                try:
                    output = available_tools[tool_name].get('fn')(tool_input)
                    messages.append({ 'role': 'assistant', 'content': json.dumps({ 'step': 'observe', 'output': output }) })
                except Exception as e:
                    print(f"❌: {e}")
                    messages.append({ 'role': 'assistant', 'content': json.dumps({ 'step': 'error', 'output': e }) })
                continue

        if parsed_output['step'] == 'output':
            print(f"🤖: {parsed_output.get('content')}")
            break
