import os
from openai import AzureOpenAI
from dotenv import load_dotenv

systemprompt = """
# ROLE
You are the autonomous control system for an exploration robot operating in an unknown environment. 

# OBJECTIVE
You will receive detailed mission instructions. Navigate the environment to complete the objective. 

# AVAILABLE COMMANDS
You are restricted to the following exact function calls:
- move_forward(distance_in_meters)
- turn(angle_in_degrees)  // Positive = counter-clockwise, Negative = clockwise
- finish(reason) // Ends mission. Call when complete.
- # Comment (starting with #)

# CRITICAL EXECUTION RULES
1. Sequential Execution: Commands are executed in the exact order you list them.
2. I need to keep a distance of at least one unit to all objects. So do not drive into objects.

# OUTPUT FORMAT
You must format your response using XML tags. 
First, use a <thought> block to briefly plan your route based on your last sensor readings. 
Then, use an <actions> block to list your commands, one per line. Do not include anything else.

Example Output:
<thought>
My objective is to find a green object and walk around it. My info tells me that a green object is 5 units away from me at an angle of 20°.
To walk around it, i must first turn 20°, then move forward 4 units so I am close to the object.
To start walking around it, I need to turn until I am parallel to the object.
I then need to move forward and make 90° turns multiple times until I have walked completely around the object.

</thought>
<actions>
turn(20)
move_forward(4.0)
# I am now in front of the object. I have to turn to align myself for the walk around
turn(-20)
# I am now parallel to the object. I will begin walking around it
move_forward(2)
turn(90)
move_forward(2)
turn(-90)
move_forward(2)
turn(90)
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

    def instruct(self, task):

        task += "\n So far you have executed the following commands: "
        for command in self.command_history:
            task += f"{command}\n"

        self.messages.append({"role": "user", "content": task})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        return response.choices[0].message.content

    def instruct_with_image(self, task, base64_image):
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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        return response.choices[0].message.content

    def add_command_to_history(self, command):
        self.command_history.append(command)
