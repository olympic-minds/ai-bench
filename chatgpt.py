from chat import Chat
from dotenv import load_dotenv
import openai
import os


class ChatGPT(Chat):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        load_dotenv()
        OPENAI_KEY = os.getenv("OPENAI_KEY")
        self.client = openai.OpenAI(api_key=OPENAI_KEY)
        self.model = model
        pass

    def prompt(self, system_prompt: str, message: str, temperature: float = 0.2) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content
