"""
agent.py

LangGraph Agent with short-term conversation memory.
"""

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool

from src.llm import GeminiLLM

from src.mcp_tool_client import (
    expense_lookup,
    eligibility_lookup,
    approval_lookup,
    airport_lookup,
    cancellation_lookup,
)


# ---------------------------------------------------------
# MCP Tools exposed to the LangGraph agent
# ---------------------------------------------------------

@tool
def expense_tool(country: str, amount: float) -> str:
    """
    Get expense reimbursement policy for a country and amount.
    """
    return expense_lookup(country, amount)


@tool
def eligibility_tool(employee_id: str) -> str:
    """
    Check employee travel eligibility.
    """
    return eligibility_lookup(employee_id)


@tool
def approval_tool(
    employee_id: str,
    country: str,
    amount: float,
) -> str:
    """
    Check whether travel approval is required.
    """
    return approval_lookup(
        employee_id,
        country,
        amount,
    )


@tool
def airport_tool(country: str) -> str:
    """
    Get airport travel policy for a country.
    """
    return airport_lookup(country)


@tool
def cancellation_tool(stage: str) -> str:
    """
    Get cancellation policy for a specific travel stage.
    """
    return cancellation_lookup(stage)


# ---------------------------------------------------------
# List of tools available to the agent
# ---------------------------------------------------------

tools = [
    expense_tool,
    eligibility_tool,
    approval_tool,
    airport_tool,
    cancellation_tool,
]


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = GeminiLLM().llm


# ---------------------------------------------------------
# Short-term conversation memory
# ---------------------------------------------------------

memory = InMemorySaver()


# ---------------------------------------------------------
# LangGraph Agent
# ---------------------------------------------------------

agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,
)