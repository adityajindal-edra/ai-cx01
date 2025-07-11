import os
import anthropic
from llm_clients.client_interface import ClientInterface

from dotenv import load_dotenv

load_dotenv()
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL")


class ClaudeClient(ClientInterface):
    def __init__(self, prompt_file, output_file):
        self.prompt_file = prompt_file
        self.output_file = output_file
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.conversation_history = []


    def read_parse_prompt(self, original_conversation: str):
        with open(self.prompt_file, "r") as f:
            template = f.read().strip()
        return template.replace("{{ USER_CONVERSATION }}", original_conversation)

    def read_prompt(self, error: str):
        with open(self.prompt_file, "r") as f:
            template = f.read().strip()
        return template.replace("{{ USER_ERROR_MESSAGE }}", error)

    def send_message_to_llm(self, message):
        self.conversation_history.append(
            {"role": "user", "content": [{"type": "text", "text": message}]}
        )

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=20000,
            messages=self.conversation_history,
            temperature=1,
        )

        assistant_response = response.content[0].text if response.content else ""

        self.conversation_history.append(
            {
                "role": "assistant",
                "content": [{"type": "text", "text": assistant_response}],
            }
        )

        return assistant_response

    def reset_conversation(self):
        self.conversation_history = []

    def save_response(self, response):
        with open(self.output_file, "w") as f:
            f.write(response)

    def update_output_file(self, new_output_file):
        self.output_file = new_output_file
