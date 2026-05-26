import os
import config
from openai import AzureOpenAI
from dotenv import load_dotenv

systemprompt = f"""
# ROLE
You are a navigation assistant, planning the route of a robot to complete a task

# SENSOR INFO
You will receive info about the relative distance and angle of objects in your vicinity.
Angles are in {config.unit_angle}
Angles increase counter-clockwise, e.g. 20 degrees is to your left, -30 to your right.

# TASK
Draw a map of your environment for each step you take.
If multiple steps are necessary to complete the task, draw a new map after each step.
Possible steps are moving forward x meters and turning right/left x degrees.

# OUTPUT FORMAT
You MUST format your output as a 10 x 10 grid of characters.
Use . for free space and # for objects. Mark your own position with a X.
Assume you position in the center of the grid.

# EXAMPLE

## Task:

Walk around the right object.

## Output:

Initial position

..........
..........
..#....#..
..........
..........
.....X....
..........
..........
..........
..........

Turn 1:

..........
.....X....
..#....#..
..........
..........
..........
..........
..........
..........
..........

Turn 2:

..........
........X.
..#....#..
..........
..........
..........
..........
..........
..........
..........

Turn 3:

..........
..........
..#....#..
........X.
..........
..........
..........
..........
..........
..........

Turn 4:

..........
..........
..#....#..
.....X....
..........
..........
..........
..........
..........
..........

DONE

"""

MODEL_GPT_5_MINI = "gpt-5-mini"
MODEL_GPT_5_2_CHAT = "gpt-5.2-chat"
MODEL_GPT_4o = "gpt-4o"
MODEL_GPT_4_1 = "gpt-4.1"
MODEL_GPT_4_1_MINI = "gpt-4.1-mini"
MODEL_DEEPSEEK = "DeepSeek-V3.2"

class DrawOperator:
    def __init__(self):
        load_dotenv("azure.env")
        self.client = AzureOpenAI(
            api_version="2025-03-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        self.model = MODEL_GPT_5_2_CHAT
        self.messages = [
            {"role": "system", "content": systemprompt},
        ]
        self.command_history = []
        self.task_history = []

    def instruct(self, task):

        if len(self.command_history) > 0:
            task += "\n So far you have executed the following commands: "
            for command in self.command_history:
                task += f"{command}\n"

        self.messages.append({"role": "user", "content": task})
        self.task_history.append(task)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        return response.choices[0].message.content

    def instruct_with_image(self, task, base64_image):
        if len(self.command_history) > 0:
            task += "\n So far you have executed the following commands: "
            for command in self.command_history:
                task += f"{command}\n"

        self.messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": task},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]
        })
        self.task_history.append(task)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        return response.choices[0].message.content

    def add_command_to_history(self, command):
        self.command_history.append(command)
    
    def get_command_history(self):
        return self.command_history

    def get_system_prompt(self):
        return systemprompt

    def get_model(self):
        return self.model
