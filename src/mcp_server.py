"""
mcp_server.py

Uber AI Travel Policy MCP Server
"""

from mcp.server import MCPServer
import logging
from src.tools import (
    expense_policy_lookup,
    employee_eligibility,
    travel_approval,
    airport_policy,
    cancellation_policy,
)

# Create MCP Server
mcp = MCPServer(
    "Uber Travel Policy Assistant",
    instructions="Answer Uber Business travel policy questions using the available tools."
)


@mcp.tool()
def get_expense_policy(country: str, amount: float) -> str:
    """
    Retrieve the expense reimbursement policy.
    """
    return expense_policy_lookup.invoke(
        {
            "country": country,
            "amount": amount,
        }
    )

@mcp.tool()
def get_employee_eligibility(employee_id: str) -> str:
    """Check employee eligibility."""
    return employee_eligibility.invoke(
        {
            "employee_id": employee_id
        }
    )

@mcp.tool()
def get_travel_approval(
    employee_id: str,
    country: str,
    amount: float,
) -> str:
    """Check travel approval."""
    return travel_approval.invoke(
        {
            "employee_id": employee_id,
            "country": country,
            "amount": amount,
        }
    )

@mcp.tool()
def get_airport_policy(country: str) -> str:
    """Airport travel policy."""
    return airport_policy.invoke(
        {
            "country": country,
        }
    )

@mcp.tool()
def get_cancellation_policy(stage: str) -> str:
    """Cancellation policy."""
    return cancellation_policy.invoke(
        {
            "stage": stage,
        }
    )

if __name__ == "__main__":
    

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Starting MCP Server...")
    mcp.run(
    transport="streamable-http",
    host="127.0.0.1",
    port=8000,)