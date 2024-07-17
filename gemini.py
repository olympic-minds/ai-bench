from chat import Chat
from dotenv import load_dotenv
import google.generativeai as genai
import os


class Gemini(Chat):
    def __init__(self, model: str = "gemini-1.5-pro"):
        load_dotenv()
        GOOGLE_KEY = os.getenv("GOOGLE_KEY")
        genai.configure(api_key=GOOGLE_KEY)
        self.client = genai.GenerativeModel(model)
        pass

    def prompt(self, system_prompt: str, message: str) -> str:
        chat = self.client.start_chat(
            history=[{"role": "user", "parts": [system_prompt]}]
        )
        response = chat.send_message(message)
        return response.text
