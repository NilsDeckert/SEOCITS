import os
from openai import AzureOpenAI
from dotenv import load_dotenv

#systemprompt = """
#You are the operator of an exploration robot in an unknown environment.
#You are controlling a robot that is equipped with a simple lidar sensor and a camera.
#You will receive detailled intructions about your exploration job.
#To complete your mission, you have the following commands available:
#- move_forward(distance_in_meters)
#- turn(angle_in_degrees)
#- get_lidar_scan()
#- get_rgb_image()
#- finish(reason)
#
#Lidar value of 5.0 or higher away are out of reach for the sensor. There might still be objects in that direction.
#get_rgb_image() will show you the POV of the robot.
#
#Calling get_lidar_scan() or get_rgb_image() will reset the queue of commands to be executed. So do not list commands after get_lidar_scan() or get_rgb_image() if you want them to be executed.
#
#Calling turn() with positive degrees will turn the robot counter-clockwise.
#Calling turn() with negative degrees will turn the robot clockwise.
#
#Only ever return calls to the functions specified above.
#Do not write any comments or explanations. 
#Do not ask questions.
#Double check that you only use the functions above.
#Once you completet your target, call the finish() function to end the mission.
#"""

systemprompt = """
# ROLE
You are the autonomous control system for an exploration robot operating in an unknown environment. 

# OBJECTIVE
You will receive detailed mission instructions. Navigate the environment, gather necessary sensor data, and complete the objective.

# AVAILABLE COMMANDS
You are restricted to the following exact function calls:
- move_forward(distance_in_meters)
- turn(angle_in_degrees)  // Positive = counter-clockwise, Negative = clockwise
- get_lidar_scan()        // Returns 2D distance. Values >= 5.0m mean clear space up to 5m.
- get_rgb_image()         // Returns the front-facing POV of the robot.
- finish(success=True/False, reason="...") // Ends mission. Call when complete.

# SENSOR DATA FORMATS
When you call get_lidar_scan(), you will receive an array of 8 float values. 
- These values represent distances in meters. 
- The array starts directly in front of the robot (0 degrees) and sweeps counter-clockwise in 45-degree increments.
- Index mapping: [0° (Front), 45° (Left-Front), 90° (Left), 135° (Left-Rear), 180° (Rear), 225° (Right-Rear), 270° (Right), 315° (Right-Front)].
- A value of 5.0 means the space is clear up to the sensor's maximum range.

# CRITICAL EXECUTION RULES
1. Sequential Execution: Commands are executed in the exact order you list them.
2. The Sensor Interrupt Rule: Calling `get_lidar_scan()` or `get_rgb_image()` immediately halts the current execution queue to return data to you. 
3. Because of Rule 2, a sensor command MUST be the absolutely LAST command in your `<actions>` block. Any commands placed after a sensor call will be completely ignored.

# OUTPUT FORMAT
You must format your response using XML tags. 
First, use a <thought> block to briefly plan your route based on your last sensor readings. 
Then, use an <actions> block to list your commands, one per line. Do not include anything else.

Example Output:
<thought>
The lidar scan showed an obstacle 1.2 meters directly ahead. I need to turn 90 degrees clockwise to navigate around it, move forward, and take another scan to assess the new corridor.
</thought>
<actions>
turn(-90)
move_forward(2.0)
get_lidar_scan()
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
