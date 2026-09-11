"""
chunking.py

Contains functions for splitting documents into chunks
for Retrieval-Augmented Generation (RAG).
"""

import json
from pathlib import Path
from src.config import CHUNK_SIZE, CHUNK_OVERLAP
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: list,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list:
    """
    Split documents into smaller chunks while preserving metadata.

    Parameters
    ----------
    documents : list
        List of loaded documents.

    chunk_size : int
        Maximum size of each chunk.

    chunk_overlap : int
        Number of overlapping characters between chunks.

    Returns
    -------
    list
        List of chunk dictionaries.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for document in documents:

        split_text = splitter.split_text(document["content"])

        for index, chunk in enumerate(split_text):

            chunk_metadata = document["metadata"].copy()

            chunk_metadata.update({
                    "chunk_number": index,
                    "chunk_size": len(chunk),
                    "document_length": len(document["content"]),
                    "total_chunks": len(split_text),
                })

            chunks.append(
                {
                    "chunk_id": f"{document['filename']}_{index}",
                    "filename": document["filename"],
                    "text": chunk,
                    "metadata": chunk_metadata,
                }
            )

    total_chars = sum(len(c["text"]) for c in chunks)
    avg_chunk = total_chars / len(chunks)

    print("\nChunk Statistics")
    print("-" * 40)
    print(f"Total Chunks   : {len(chunks)}")
    print(f"Average Size   : {avg_chunk:.2f} characters")
    print(f"Largest Chunk  : {max(len(c['text']) for c in chunks)}")
    print(f"Smallest Chunk : {min(len(c['text']) for c in chunks)}")

    return chunks

    return chunks


def save_chunks(
    chunks: list,
    output_file: str = "data/processed/chunks.json",
):
    """
    Save generated chunks as a JSON file.
    """

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("\nChunk File Created Successfully")
    print("-" * 40)
    print(f"Chunks Saved : {len(chunks)}")
    print(f"Location     : {output_path}")