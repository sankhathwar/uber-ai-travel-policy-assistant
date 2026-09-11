"""
agent.py

LangGraph Agent
"""

from langgraph.prebuilt import create_react_agent
from langchain.tools import tool

from src.llm import GeminiLLM
from src.mcp_tool_client import (
    expense_lookup,
    eligibility_lookup,
    approval_lookup,
    airport_lookup,
    cancellation_lookup,
)

from src.mcp_tool_client import (
    expense_lookup,
    eligibility_lookup,
    approval_lookup,
    airport_lookup,
    cancellation_lookup,
)

@tool
def expense_tool(country: str, amount: float) -> str:
    """
    Get expense policy.
    """
    return expense_lookup(country, amount)


@tool
def eligibility_tool(employee_id: str) -> str:
    """
    Check employee eligibility.
    """
    return eligibility_lookup(employee_id)


@tool
def approval_tool(
    employee_id: str,
    country: str,
    amount: float,
) -> str:
    """
    Check travel approval.
    """
    return approval_lookup(
        employee_id,
        country,
        amount,
    )


@tool
def airport_tool(country: str) -> str:
    """
    Airport travel policy.
    """
    return airport_lookup(country)


@tool
def cancellation_tool(stage: str) -> str:
    """
    Cancellation policy.
    """
    return cancellation_lookup(stage)


tools = [
    expense_tool,
    eligibility_tool,
    approval_tool,
    airport_tool,
    cancellation_tool,
]

llm = GeminiLLM().llm

agent = create_react_agent(
    model=llm,
    tools=tools,
)