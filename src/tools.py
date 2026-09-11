"""
tools.py

LangChain tools for the Uber AI Travel Policy Assistant.
"""

from langchain_core.tools import tool
from src.retriever import PolicyRetriever


# Load retriever only once
retriever = PolicyRetriever()


def retrieve_policy(query: str) -> str:
    """
    Helper function to retrieve relevant policy chunks.
    """

    documents = retriever.search(query)

    context = ""

    for doc, score in documents:

        context += (
            f"Source: {doc.metadata.get('source')}\n"
            f"Policy Type: {doc.metadata.get('policy_type')}\n"
            f"Country: {doc.metadata.get('country')}\n"
            f"Similarity Score: {score:.4f}\n\n"
            f"{doc.page_content}\n\n"
            "---------------------------------------------\n"
        )

    return context


@tool
def expense_policy_lookup(country: str, amount: float) -> str:
    """
    Retrieve expense reimbursement policy.
    """

    query = (
        f"What is the expense reimbursement policy "
        f"for {amount} in {country}?"
    )

    return retrieve_policy(query)


@tool
def employee_eligibility(employee_id: str) -> str:
    """
    Retrieve employee eligibility policy.
    """

    query = (
        f"What is the travel eligibility for employee "
        f"{employee_id}?"
    )

    return retrieve_policy(query)


@tool
def travel_approval(country: str, amount: float, employee_id: str) -> str:
    """
    Retrieve travel approval policy.
    """

    query = (
        f"Does employee {employee_id} need approval "
        f"for a {amount} ride in {country}?"
    )

    return retrieve_policy(query)


@tool
def airport_policy(country: str) -> str:
    """
    Retrieve airport travel policy for a country.
    """

    query = (
        f"What is the airport travel policy in {country}?"
    )

    return retrieve_policy(query)


@tool
def cancellation_policy(stage: str) -> str:
    """
    Retrieve cancellation policy.
    """

    query = (
        f"What is the cancellation policy for {stage}?"
    )

    return retrieve_policy(query)