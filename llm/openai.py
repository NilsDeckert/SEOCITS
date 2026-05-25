import os
from openai import AzureOpenAI
from dotenv import load_dotenv

systemprompt = """
# ROLE
You are a developer, writing code to control a robot in an unknown environment.

# AVAILABLE COMMANDS
You are restricted to the following exact function calls:
- move_forward(distance_in_meters)
- turn_right(angle_in_degrees)
- turn_left(angle_in_degrees)
- finish(reason) // Ends mission. Call when complete.

# CRITICAL EXECUTION RULES
1. Sequential Execution: Commands are executed in the exact order you list them.
2. Unless instructed otherwise, keep a distance of 1 meter to not drive into objects.

# SENSOR INFO
You will receive info about the distance and angle of objects in your vicinity.
Angles increase counter-clockwise, e.g. 20 degrees is to your left, -30 to your right.

# OUTPUT FORMAT
You must format your response using XML tags. 
First, use a <thought> block to plan your route based on your environment info.
Then, use an <actions> block to list your commands, one per line.
Include comments starting with #.

Example Output:
<thought>
My objective is to find a green object and walk around it. My info tells me that a green object is 5 meters away from me at an angle of 20 degrees.
To walk around it, i must first turn left 20 degrees then move forward 4 meters so I am close to the object.
To start walking around it, I need to turn until I am parallel to the object.
I then need to move forward and make 90 degrees turns in the direction of the object multiple times until I have walked completely around the object.

</thought>
<actions>
turn_left(20)
move_forward(4.0)
# I am now in front of the object. I have to turn to align myself for the walk around
turn_right(20)
# I am now parallel to the object. I will begin walking around it
move_forward(2)
# The object is now to my left. To walk around it, I need to turn left.
turn_left(90)
move_forward(2)
# The object is still to my left
turn_left(90)
move_forward(2)
turn_left(90)
move_forward(2)

finish("I have walked around the green object.")
</actions>
"""

MODEL_GPT_5_MINI = "gpt-5-mini"
MODEL_GPT_5_2_CHAT = "gpt-5.2-chat"
MODEL_GPT_4o = "gpt-4o"
MODEL_GPT_4_1 = "gpt-4.1"
MODEL_GPT_4_1_MINI = "gpt-4.1-mini"
MODEL_DEEPSEEK = "DeepSeek-V3.2"
MODEL_KIMI = "Kimi-K2.5"

class OpenAIOperator:
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
