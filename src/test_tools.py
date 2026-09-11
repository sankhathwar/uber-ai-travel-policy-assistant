from tools import (
    expense_policy_lookup,
    airport_policy,
    employee_eligibility,
)

print("=" * 60)

print(
    expense_policy_lookup.invoke(
        {
            "country": "India",
            "amount": 1800,
        }
    )
)

print("=" * 60)

print(
    airport_policy.invoke(
        {
            "airport": "Bangalore Airport",
        }
    )
)

print("=" * 60)

print(
    employee_eligibility.invoke(
        {
            "employee_id": "EMP002",
        }
    )
)