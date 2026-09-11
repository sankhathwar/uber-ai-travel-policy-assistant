"""
embeddings.py

Generate embeddings for policy document chunks
using Sentence Transformers.
"""

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from src.config import (
    CHUNKS_FILE,
    EMBEDDING_MODEL,
)

import os

SYSTEM_CA = "/etc/ssl/certs/ca-certificates.crt"

os.environ["REQUESTS_CA_BUNDLE"] = SYSTEM_CA
os.environ["SSL_CERT_FILE"] = SYSTEM_CA
os.environ["CURL_CA_BUNDLE"] = SYSTEM_CA

print("Using certificate bundle:", SYSTEM_CA)

class EmbeddingGenerator:
    """
    Generate embeddings for text chunks.
    """

    def __init__(self):

        print(f"\nLoading embedding model: {EMBEDDING_MODEL}")

        self.model = SentenceTransformer(EMBEDDING_MODEL)

        print("✓ Model Loaded Successfully")

    def load_chunks(self):
        """
        Load chunks from JSON.
        """

        if not Path(CHUNKS_FILE).exists():
            raise FileNotFoundError(
                f"Chunks file not found: {CHUNKS_FILE}"
            )

        with open(
            CHUNKS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            chunks = json.load(file)

        print(f"\nLoaded {len(chunks)} chunks")

        return chunks

    def generate_embeddings(self, chunks):
        """
        Generate embeddings for all chunks.
        """

        texts = [chunk["text"] for chunk in chunks]

        print("\nGenerating embeddings...")

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
        )

        print("✓ Embeddings Generated")

        return embeddings

    def run(self):

        chunks = self.load_chunks()

        embeddings = self.generate_embeddings(chunks)

        print("\nEmbedding Summary")
        print("-" * 40)
        print(f"Chunks          : {len(chunks)}")
        print(f"Embedding Shape : {embeddings.shape}")

        return chunks, embeddings


def main():

    generator = EmbeddingGenerator()

    generator.run()


if __name__ == "__main__":
    main()