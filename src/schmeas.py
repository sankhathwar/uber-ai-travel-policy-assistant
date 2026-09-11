"""
schemas.py

Pydantic schemas for validating tool inputs.
"""

from pydantic import BaseModel, Field


class ExpenseRequest(BaseModel):
    """
    Validate an expense request.
    """

    country: str = Field(
        description="Country where the trip occurred."
    )

    amount: float = Field(
        description="Expense amount."
    )


class EligibilityRequest(BaseModel):
    """
    Validate employee eligibility.
    """

    employee_id: str = Field(
        description="Employee ID."
    )


class TravelApprovalRequest(BaseModel):
    """
    Validate travel approval requests.
    """

    country: str

    amount: float

    employee_id: str


class AirportPolicyRequest(BaseModel):
    """
    Airport policy lookup.
    """

    airport: str


class CancellationRequest(BaseModel):
    """
    Cancellation policy lookup.
    """

    stage: str