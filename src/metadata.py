"""
metadata.py

Contains functions for generating metadata for policy documents.
"""


def create_metadata(filename: str) -> dict:
    """
    Generate metadata based on the document filename.

    Parameters
    ----------
    filename : str
        Name of the policy document.

    Returns
    -------
    dict
        Metadata associated with the document.
    """

    filename = filename.lower()

    metadata = {
        "source": filename,
        "policy_type": "general",
        "country": "Global"
    }

    # Country Detection
    if "india" in filename:
        metadata["country"] = "India"

    elif "us" in filename:
        metadata["country"] = "US"

    # Policy Type Detection
    if "travel" in filename:
        metadata["policy_type"] = "travel"

    elif "airport" in filename:
        metadata["policy_type"] = "airport"

    elif "expense" in filename:
        metadata["policy_type"] = "expense"

    elif "approval" in filename:
        metadata["policy_type"] = "approval"

    elif "eligibility" in filename:
        metadata["policy_type"] = "eligibility"

    elif "cancellation" in filename:
        metadata["policy_type"] = "cancellation"

    return metadata