import os
from openai import AzureOpenAI
from dotenv import load_dotenv

systemprompt = """
You are the operator of an exploration robot in an unknown environment.
You are controlling a robot that is equipped with a simple lidar sensor and a camera.
You will receive detailled intructions about your exploration job.
To complete your mission, you have the following commands available:
- move_forward(distance_in_meters)
- turn(angle_in_degrees)
- get_lidar_scan()
- get_rgb_image()
- finish(success=True, reason="")

Only ever return calls to the functions specified above.
Do not write any comments or explanations. 
Do not ask questions.
Double check that you only use the functions above.
Once you completet your target, call the finish() function to end the mission.
"""

class OpenAIOperator:
    def __init__(self):
        load_dotenv("azure.env")
        self.client = AzureOpenAI(
            api_version="2025-03-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        self.model = "gpt-5-mini"

    def new_mission(self, task):
        response = self.client.responses.create(
            model=self.model,
            instructions = systemprompt,
            input = task
        )
        return response.output_text
