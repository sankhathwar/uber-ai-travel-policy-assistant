"""
mcp_tool_client.py

Wrapper functions for calling MCP tools.
"""

import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

SERVER_URL = "http://127.0.0.1:8000/mcp"


async def call_tool(tool_name: str, arguments: dict):

    async with streamable_http_client(
        SERVER_URL
    ) as (read_stream, write_stream):

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments,
            )

            # Uncomment for debugging
            # print(result)

            # MCP 2.x may return structured content
            if (
                hasattr(result, "structured_content")
                and result.structured_content
            ):
                if isinstance(result.structured_content, dict):
                    return result.structured_content.get(
                        "result",
                        str(result.structured_content),
                    )

                return str(result.structured_content)

            # Otherwise return normal text
            if (
                hasattr(result, "content")
                and result.content
            ):
                return "\n".join(
                    item.text
                    for item in result.content
                    if hasattr(item, "text")
                )

            return str(result)


def expense_lookup(country, amount):
    return asyncio.run(
        call_tool(
            "get_expense_policy",
            {
                "country": country,
                "amount": amount,
            },
        )
    )


def eligibility_lookup(employee_id):
    return asyncio.run(
        call_tool(
            "get_employee_eligibility",
            {
                "employee_id": employee_id,
            },
        )
    )


def approval_lookup(employee_id, country, amount):
    return asyncio.run(
        call_tool(
            "get_travel_approval",
            {
                "employee_id": employee_id,
                "country": country,
                "amount": amount,
            },
        )
    )


def airport_lookup(country):
    return asyncio.run(
        call_tool(
            "get_airport_policy",
            {
                "country": country,
            },
        )
    )


def cancellation_lookup(stage):
    return asyncio.run(
        call_tool(
            "get_cancellation_policy",
            {
                "stage": stage,
            },
        )
    )