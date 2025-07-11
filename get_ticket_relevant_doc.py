from sqlalchemy import create_engine, Column, func, text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import VARCHAR, Float
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import declarative_base
import numpy as np
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

TICKETS_DATABASE_URL = "postgresql://localhost:5432/freshdesk_updated5"  # Update with your credentials
DOCS_DATABASE_URL = "postgresql://localhost:5432/bs_docs"  # Update with your credentials

class LangchainPgEmbedding(declarative_base()):
    __tablename__ = 'langchain_pg_embedding'

    id = Column(VARCHAR, primary_key=True)  # Assuming 'id' is unique
    collection_id = Column(UUID(as_uuid=True), nullable=False)
    embedding = Column(Vector(3072))  # Updated to match actual dimensions
    document = Column(VARCHAR)
    cmetadata = Column(JSONB)

class BStackDoc(declarative_base()):
    __tablename__ = 'langchain_pg_embedding'

    id = Column(VARCHAR, primary_key=True)  # Assuming 'id' is unique
    collection_id = Column(UUID(as_uuid=True), nullable=False)
    embedding = Column(Vector(3072))  # Correct dimensions
    document = Column(VARCHAR)
    cmetadata = Column(JSONB)

class GetRelevantBstackDoc:
    def __init__(self, ticket_id: str):
        self.ticket_id = ticket_id
        self.ticket_engine = create_engine(TICKETS_DATABASE_URL)
        self.TicketSession = sessionmaker(bind=self.ticket_engine)
        self.docs_engine = create_engine(DOCS_DATABASE_URL)
        self.DocsSession = sessionmaker(bind=self.docs_engine)

    def get_ticket_data(self):
        with self.TicketSession() as session:
            result = session.query(
                LangchainPgEmbedding.id,
                LangchainPgEmbedding.collection_id,
                LangchainPgEmbedding.embedding,
                LangchainPgEmbedding.document,
                LangchainPgEmbedding.cmetadata
            ).filter(LangchainPgEmbedding.id == self.ticket_id).first()

        return result

    def get_relevant_docs(self, limit=100, similarity_threshold=0.7):
        ticket_data = self.get_ticket_data()

        if not ticket_data or not ticket_data.document:
            print(f"No document found for ticket ID: {self.ticket_id}")
            return []

        # Get embeddings for the ticket document using OpenAI's API
        response = openai.embeddings.create(
            input=ticket_data.document,
            model="text-embedding-3-large",
            dimensions=3072
        )

        ticket_embedding = response.data[0].embedding

        # Format the embedding as a string with the required format
        ticket_embedding_str = str(ticket_embedding).replace('[', "[").replace("]", "]")

        with self.DocsSession() as session:
            # Use raw SQL query with the pgvector <=> operator for cosine distance
            raw_sql = text("""
            SELECT langchain_pg_embedding.id AS langchain_pg_embedding_id,
                   langchain_pg_embedding.document AS langchain_pg_embedding_document,
                   langchain_pg_embedding.cmetadata AS langchain_pg_embedding_cmetadata,
                   langchain_pg_embedding.embedding <=> :embedding AS distance
            FROM langchain_pg_embedding
            ORDER BY distance ASC
            LIMIT :limit
            """)

            results = session.execute(raw_sql, {
                'embedding': ticket_embedding_str,
                'limit': limit
            }).fetchall()

            relevant_docs = [
                {
                    'id': doc.langchain_pg_embedding_id,
                    'document': doc.langchain_pg_embedding_document,
                    'metadata': doc.langchain_pg_embedding_cmetadata,
                    'similarity': 1 - doc.distance  # Convert distance back to similarity
                }
                for doc in results
                if (1 - doc.distance) >= similarity_threshold  # Convert to similarity for threshold
            ]

        return relevant_docs
if __name__ == "__main__":
    ticket_ids = ['61fd6a97-d055-4b44-9a74-dbcbe604b371', '39d5b40b-5862-45cc-92c2-7282d75fb6f9', '3468574d-dc4e-4c8c-8ab4-b3228a16eea6', '536ab2ba-ff01-4fad-8274-c1b3a6f4df85', 'b25d2359-7735-458b-aeed-22fd82ca92f9', 'fc88b408-380a-472d-98ef-27cd53f61c98', 'ffa00dea-8ae5-4f20-8ebf-8854cb1dffbb', '0fd4a05a-e184-4727-a0a0-40a36eb9ebaf', '1fb80e04-ad59-4ba0-86c4-db1619b04588', '94301067-3a6a-46e3-9fb2-00c7427de4ab']

    for ticket_id in ticket_ids:
        retriever = GetRelevantBstackDoc(ticket_id)
        relevant_docs = retriever.get_relevant_docs(limit=10000, similarity_threshold=0.5)
        ticket_doc = ""
        for doc in relevant_docs[:500]:
            ticket_doc += doc['document'] + "\n"
        with open(f"{ticket_id}_relevant_docs.txt", 'w') as f:
            f.write(ticket_doc)


