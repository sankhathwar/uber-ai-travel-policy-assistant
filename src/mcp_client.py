"""
mcp_client.py

Test client for the Uber Travel Policy MCP Server
"""

import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():

    async with streamable_http_client(
        "http://127.0.0.1:8000/mcp"
    ) as (read_stream, write_stream):

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            # Initialize connection
            await session.initialize()

            # List all available tools
            tools = await session.list_tools()

            print("\nAvailable Tools")
            print("=" * 50)

            for tool in tools.tools:
                print(f"- {tool.name}")

            print("\nCalling get_expense_policy...\n")

            result = await session.call_tool(
                "get_expense_policy",
                {
                    "country": "India",
                    "amount": 1800,
                },
            )

            print(result)


if __name__ == "__main__":
    asyncio.run(main())