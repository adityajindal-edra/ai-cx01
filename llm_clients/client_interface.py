from abc import ABC, abstractmethod


class ClientInterface(ABC):
    @abstractmethod
    def read_prompt(self, error: str):
        """Reads the prompt from a file and replaces placeholders with the provided error message."""
        pass

    @abstractmethod
    def send_message_to_llm(self, message: str):
        """Sends the prompt to the LLM and returns the response."""
        pass

    @abstractmethod
    def reset_conversation(self):
        """Resets the conversation history."""
        pass

    @abstractmethod
    def save_response(self, response: str):
        """Saves the LLM response to the output file."""
        pass

    @abstractmethod
    def update_output_file(self, new_output_file: str):
        """Updates the output file path."""
        pass
