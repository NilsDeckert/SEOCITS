from llm import Task
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

systemprompt = """
You are an advanced robot control specialist.
Your job is to review the robot control instructions written by a junior developer for a given task.

Angles increase clockwise and decrease counter-clockwise

# AVAILABLE COMMANDS
You are restricted to the following exact function calls:
- move_forward(distance_in_meters)
- turn_right(angle_in_degrees)
- turn_left(angle_in_degrees)
- finish(reason) // Ends mission. Call when complete.

# OUTPUT
You must format your response using XML tags. 
First, use a <thought> block to assess the proposed commands and plan your adjustments.
Then, use an <actions> block to list your final list of commands, one per line.
"""

MODEL_GPT_5_MINI = "gpt-5-mini"
MODEL_GPT_5_2_CHAT = "gpt-5.2-chat"
MODEL_GPT_5_3_CHAT = "gpt-5.3-chat"
MODEL_GPT_4o = "gpt-4o"
MODEL_GPT_4_1 = "gpt-4.1"
MODEL_GPT_4_1_MINI = "gpt-4.1-mini"
MODEL_DEEPSEEK = "DeepSeek-V3.2"
MODEL_KIMI = "Kimi-K2.5"

class Reviewer:
    """
    The purpose of the class is to take an existing Task and review
    a proposed list of commands to fulfull the task.
    """
    def __init__(self, model: str = MODEL_GPT_5_3_CHAT):
        load_dotenv("azure.env")
        self.client = AzureOpenAI(
            api_version="2025-03-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        self.model = model
        self.messages = [
            {"role": "system", "content": systemprompt},
        ]
        self.command_history = []
        self.task_history = []

    def review(self, proposal: Task, commands: list[str]):

        task = (
            "Given the following task: " + proposal.get_task()
            + " here is a proposal of commands to execute: "
            + "\n -".join(commands)
            + "\n Review these commands and provide an improved list of commands that will achieve the task."
        )

        self.messages.append({"role": "user", "content": task})
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
