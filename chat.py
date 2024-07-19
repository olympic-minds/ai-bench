from abc import ABC, abstractmethod
from typing import List


class Chat(ABC):
    @abstractmethod
    def __init__(self, model: str, system_prompt: str):
        self.client = None
        self.model = model
        pass

    @abstractmethod
    def prompt(self, message: str, completions: int = 1) -> List[str]:
        """
        This method should take a message as input and return a responses.

        :param message: The message to prompt the virtual assistant with.
        :param completions: Number of completions to generate.
        :return: The response from the virtual assistant.
        """
        pass
