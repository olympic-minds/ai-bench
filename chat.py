from abc import ABC, abstractmethod


class Chat(ABC):
    def __init__(self, model: str):
        self.client = None
        self.model = model
        pass

    @abstractmethod
    def prompt(self, system_prompt: str, message: str) -> str:
        """
        This method should take a message as input and return a response.

        :param message: The message to prompt the virtual assistant with.
        :return: The response from the virtual assistant.
        """
        pass
