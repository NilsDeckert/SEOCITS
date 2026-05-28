import config
import os
from enum import StrEnum
from openai import AzureOpenAI
from dotenv import load_dotenv

from llm.operator import Operator

class AzureModels(StrEnum):
    GPT_5_MINI = "gpt-5-mini"
    GPT_5_3_CHAT = "gpt-5.3-chat"
    DEEPSEEK = "DeepSeek-V3.2"
    KIMI = "Kimi-K2.5"

class AzureOperator(Operator):
    def __init__(self, model: str = AzureModels.GPT_5_3_CHAT):
        load_dotenv("azure.env")
        self.client = AzureOpenAI(
            api_version="2025-03-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        self.model = model
        self.messages = [
            {"role": "system", "content": self.system_prompt},
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
