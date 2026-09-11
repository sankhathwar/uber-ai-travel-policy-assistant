"""
ingestion.py

Main entry point for loading policy documents,
cleaning them, generating metadata,
chunking them, and saving the processed chunks.
"""
from collections import Counter
from pathlib import Path

from src.preprocessing import clean_text
from src.metadata import create_metadata
from src.chunking import chunk_documents, save_chunks


# Directory containing policy documents
DATA_DIR = Path("data/company_policy")


def load_documents():
    """
    Load all policy documents from the data directory.

    Returns
    -------
    list
        List of dictionaries containing filename,
        cleaned content, and metadata.
    """

    documents = []

    # Check if directory exists
    if not DATA_DIR.exists():
        print(f"❌ Directory not found: {DATA_DIR}")
        return documents

    # Read all text files
    txt_files = list(DATA_DIR.glob("*.txt"))

    if not txt_files:
        print("❌ No policy documents found.")
        return documents

    # Process each file
    for file_path in txt_files:

        try:
            raw_text = file_path.read_text(
                encoding="utf-8"
            )

            cleaned_text = clean_text(raw_text)

            if not cleaned_text:
                print(f"⚠ Skipping empty file: {file_path.name}")
                continue

            document = {
                "filename": file_path.name,
                "content": cleaned_text,
                "metadata": create_metadata(file_path.name)
            }

            documents.append(document)

        except Exception as error:
            print(f"Error reading {file_path.name}")
            print(error)

    return documents


def display_summary(documents, chunks):
    """
    Display project summary.
    """

    print("\n" + "=" * 80)
    print("UBER AI TRAVEL POLICY ASSISTANT")
    print("=" * 80)

    print(f"\nDocuments Loaded : {len(documents)}")
    print(f"Chunks Generated : {len(chunks)}")

    print("\nFirst Five Chunks")
    print("-" * 80)

    for chunk in chunks[:5]:

        print(f"""
Chunk ID :
{chunk['chunk_id']}

Metadata :
{chunk['metadata']}

Text :
{chunk['text'][:250]}

{'-'*80}
""")


def main():
    """
    Execute complete ingestion pipeline.
    """

    # Step 1
    documents = load_documents()

    if not documents:
        print("No documents loaded.")
        return

    # Step 2
    chunks = chunk_documents(documents)

    # Step 3
    save_chunks(chunks)

    # Step 4
    display_summary(documents, chunks)



    counter = Counter()

    for chunk in chunks:
        counter[chunk["metadata"]["source"]] += 1

    print("\nChunks per document")
    print("-" * 40)

    for document, count in counter.items():
        print(f"{document:<35} {count}")


if __name__ == "__main__":
    main()