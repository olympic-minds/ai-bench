from chat import Chat
from dotenv import load_dotenv
import openai
from google.api_core import retry
from typing import List
import time
import os
from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type,
)


class ChatGPT(Chat):
    def __init__(self, model: str = "gpt-3.5-turbo", system_prompt: str = ""):
        load_dotenv()
        OPENAI_KEY = os.getenv("OPENAI_KEY")
        self.client = openai.OpenAI(api_key=OPENAI_KEY)
        self.model = model
        self.system_prompt = system_prompt
        pass

    @retry(
        retry=retry_if_exception_type(openai.RateLimitError),
        wait=wait_exponential(multiplier=2, max=60),
        stop=stop_after_attempt(5),
    )
    def prompt(
        self,
        message: str,
        completions: int = 1,
        temperature: float = 0.2,
    ) -> List[str]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message},
            ],
            temperature=temperature,
            n=completions,
        )
        return [choice.message.content for choice in response.choices]
