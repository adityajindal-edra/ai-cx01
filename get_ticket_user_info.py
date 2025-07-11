import asyncio
import json

from sqlalchemy import create_engine, Column, func
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import VARCHAR
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import declarative_base
from llm_clients.claude_client import ClaudeClient

# Database configuration
DATABASE_URL = "postgresql://localhost:5432/freshdesk_updated5"  # Update with your credentials


class LangchainPgEmbedding(declarative_base()):
    __tablename__ = 'langchain_pg_embedding'

    id = Column(VARCHAR, primary_key=True)  # Assuming 'id' is unique
    collection_id = Column(UUID(as_uuid=True), nullable=False)
    embedding = Column(Vector(1536))  # or whatever dimension you use
    document = Column(VARCHAR)
    cmetadata = Column(JSONB)


class GetTicketUserInfo:
    def __init__(self, ticket_id:str):
        self.ticket_id = ticket_id
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    def get_user_info(self):
        with self.Session() as session:
            # Query to get the user information based on the ticket_id
            result = session.query(
                LangchainPgEmbedding.id,
                LangchainPgEmbedding.collection_id,
                LangchainPgEmbedding.embedding,
                LangchainPgEmbedding.document,
                LangchainPgEmbedding.cmetadata
            ).filter(LangchainPgEmbedding.id == self.ticket_id).first()

            if result:
                return {
                    "id": result.id,
                    "collection_id": str(result.collection_id),
                    "document": result.document,
                    "cmetadata": result.cmetadata
                }
            else:
                return None

async def parse_user_conversation(ticket_id: str):
    print(f"Parsing user conversation for ticket {ticket_id}...")
    user_info_fetcher = GetTicketUserInfo(ticket_id)
    user_info = user_info_fetcher.get_user_info()

    original_conversation = user_info['cmetadata']['original']

    claude_client = ClaudeClient(prompt_file="prompts/parse_user_conversation.txt",
                                 output_file=f"outputs/{ticket_id}.json")
    parse_user_conversation_prompt = claude_client.read_parse_prompt(original_conversation=original_conversation)
    user_conversation = claude_client.send_message_to_llm(message=parse_user_conversation_prompt)
    claude_client.save_response(user_conversation)

class CreateUserConversationDump:
    def __init__(self, ticket_id: str):
        self.ticket_id = ticket_id

    def create_dump(self):
        with open(f"outputs/{self.ticket_id}.json", "r") as file:
            data = json.load(file)

        user_messages = []
        for message in data['conversation']:
            if message['role'] == 'user':
                user_messages.append(message['message'])

        user_conversation = "\n".join(user_messages)
        with open(f"outputs/{self.ticket_id}_user_conversation.txt", "w") as file:
            file.write(user_conversation)


if __name__ == "__main__":
    ticket_ids = ['61fd6a97-d055-4b44-9a74-dbcbe604b371', '39d5b40b-5862-45cc-92c2-7282d75fb6f9', '3468574d-dc4e-4c8c-8ab4-b3228a16eea6', '536ab2ba-ff01-4fad-8274-c1b3a6f4df85', 'b25d2359-7735-458b-aeed-22fd82ca92f9', 'fc88b408-380a-472d-98ef-27cd53f61c98', 'ffa00dea-8ae5-4f20-8ebf-8854cb1dffbb', '0fd4a05a-e184-4727-a0a0-40a36eb9ebaf', '1fb80e04-ad59-4ba0-86c4-db1619b04588', '94301067-3a6a-46e3-9fb2-00c7427de4ab']
    for ticket_id in ticket_ids:
        # asyncio.run(parse_user_conversation(ticket_id))
        user_conversation_dump = CreateUserConversationDump(ticket_id)
        user_conversation_dump.create_dump()

