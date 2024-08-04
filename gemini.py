from chat import Chat
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import retry
from typing import List
import os


class Gemini(Chat):
    def __init__(self, model: str = "gemini-1.5-pro", system_prompt: str = ""):
        load_dotenv()
        GOOGLE_KEY = os.getenv("GOOGLE_KEY")
        genai.configure(api_key=GOOGLE_KEY)
        self.client = genai.GenerativeModel(model, system_instruction=[system_prompt])
        self.model = model
        pass

    @retry.Retry(
        predicate=retry.if_transient_error,
        initial=1.0,
        maximum=64.0,
        multiplier=2.0,
        timeout=300,
    )
    def prompt(
        self,
        message: str,
        completions: int = 1,
        temperature: float = 0.2,
    ) -> List[str]:
        # Although the gemini api provides an option candidate_count the only currently available value is 1
        candidates = []
        for i in range(completions):
            response = self.client.generate_content(
                message,
                generation_config=genai.GenerationConfig(
                    temperature=temperature, candidate_count=1
                ),
            )
            candidates.append(response.text)
        return candidates
