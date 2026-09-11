"""
vector_store.py

Creates and saves the FAISS vector store.
"""

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.config import (
    CHUNKS_FILE,
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
)
import os

SYSTEM_CA = "/etc/ssl/certs/ca-certificates.crt"

os.environ["REQUESTS_CA_BUNDLE"] = SYSTEM_CA
os.environ["SSL_CERT_FILE"] = SYSTEM_CA
os.environ["CURL_CA_BUNDLE"] = SYSTEM_CA

print("Using certificate bundle:", SYSTEM_CA)
import json


class VectorStoreBuilder:

    def __init__(self):

        print("Loading embedding model...")

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        print("✓ Embedding model loaded")

    def load_chunks(self):

        with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
            chunks = json.load(file)

        print(f"✓ Loaded {len(chunks)} chunks")

        return chunks

    def convert_to_documents(self, chunks):

        documents = []

        for chunk in chunks:

            doc = Document(
                page_content=chunk["text"],
                metadata=chunk["metadata"]
            )

            documents.append(doc)

        return documents

    def build_vector_store(self, documents):

        print("\nCreating FAISS Index...")

        vector_store = FAISS.from_documents(
            documents,
            self.embedding_model
        )

        return vector_store

    def save_vector_store(self, vector_store):

        Path(FAISS_INDEX_PATH).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        vector_store.save_local(
            str(FAISS_INDEX_PATH)
        )

        print("\n✓ Vector Store Saved")
        print(f"Location : {FAISS_INDEX_PATH}")

    def run(self):

        chunks = self.load_chunks()

        documents = self.convert_to_documents(chunks)

        vector_store = self.build_vector_store(documents)

        self.save_vector_store(vector_store)


def main():

    builder = VectorStoreBuilder()

    builder.run()


if __name__ == "__main__":
    main()