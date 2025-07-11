import os

from openai import OpenAI
from dotenv import load_dotenv

from llm_clients.client_interface import ClientInterface

load_dotenv()
GPT_MODEL = os.environ.get("GPT_MODEL")


class GPTClient(ClientInterface):
    def __init__(self, prompt_file, output_file):
        self.prompt_file = prompt_file
        self.output_file = output_file
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history = []

    def read_prompt(self, error: str):
        with open(self.prompt_file, "r") as f:
            template = f.read().strip()
        return template.replace("{{ USER_ERROR_MESSAGE }}", error)

    def send_message_to_llm(self, message):
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=self.conversation_history,
            max_tokens=10000,
            temperature=1,
            top_p=1,
        )

        assistant_response = (
            response.choices[0].message.content if response.choices else ""
        )

        # Add assistant response to history
        self.conversation_history.append(
            {"role": "assistant", "content": assistant_response}
        )

        return assistant_response

    def reset_conversation(self):
        self.conversation_history = []

    def save_response(self, response):
        with open(self.output_file, "w") as f:
            f.write(response)

    def update_output_file(self, new_output_file):
        self.output_file = new_output_file
