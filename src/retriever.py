"""
retriever.py

Loads the FAISS vector store and retrieves
the most relevant policy chunks.
"""

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.config import (
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    TOP_K_RESULTS,
)
SYSTEM_CA = "/etc/ssl/certs/ca-certificates.crt"
import os
os.environ["REQUESTS_CA_BUNDLE"] = SYSTEM_CA
os.environ["SSL_CERT_FILE"] = SYSTEM_CA
os.environ["CURL_CA_BUNDLE"] = SYSTEM_CA

print("Using certificate bundle:", SYSTEM_CA)

class PolicyRetriever:

    def __init__(self):

        print("Loading embedding model...")

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        print("Loading FAISS Vector Store...")

        self.vector_store = FAISS.load_local(
            str(FAISS_INDEX_PATH),
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

        print("✓ Vector Store Loaded")

    def search(self, query: str):

        results = self.vector_store.similarity_search_with_score(
                    query,
                    k=TOP_K_RESULTS
                )

        return results


def main():

    retriever = PolicyRetriever()

    while True:

        print("\n" + "=" * 60)

        query = input("Ask a travel policy question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        results = retriever.search(query)

        print("\nTop Matching Chunks")
        print("-" * 60)

    for i, (doc, score) in enumerate(results, start=1):

        print(f"\nResult {i}")
        print(f"Similarity Score : {score:.4f}")
        print(f"Source           : {doc.metadata['source']}")
        print(f"Policy Type      : {doc.metadata['policy_type']}")
        print(f"Country          : {doc.metadata['country']}")
        print("\nChunk")
        print(doc.page_content)


if __name__ == "__main__":
    main()