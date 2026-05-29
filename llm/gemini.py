import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from enum import StrEnum

import config
from llm.operator import Operator

class GeminiModels(StrEnum):
    PRO = "gemini-3.1-pro-preview"
    FLASH = "gemini-3.5-flash"
    LIGHT = "gemini-3.1-flash-lite"

class GeminiOperator(Operator):
    """
    LLM Operator that uses gemini models
    """
    def __init__(self, model):
        load_dotenv("google.env")
        self.model = model
        self.client = genai.Client(
            api_key=os.getenv("GOOGLE_GENAI_API_KEY"),
        )
        self.chat = self.client.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt
            )
        )

    def instruct(self, task) -> str:
        self.task_history.append(task)
        response = self.chat.send_message(task)

        if not response.text:
            raise ValueError("LLM did not deliver a response")

        return response.text

    def instruct_with_image(self, task, base64_image) -> str:
        raise NotImplemented