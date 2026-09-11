"""
preprocessing.py

Contains functions for cleaning and normalizing policy documents.
"""

import re


def clean_text(text: str) -> str:
    """
    Clean and normalize policy document text while preserving
    important formatting like headings and paragraphs.

    Parameters
    ----------
    text : str
        Raw document text.

    Returns
    -------
    str
        Cleaned document text.
    """

    if not text:
        return ""

    # Remove leading/trailing whitespace
    text = text.strip()

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Replace multiple spaces with a single space
    text = re.sub(r"[ ]{2,}", " ", text)

    # Replace 3 or more blank lines with 2 blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove trailing spaces at the end of lines
    text = "\n".join(line.rstrip() for line in text.splitlines())

    return text