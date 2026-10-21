
import asyncio
import sys

from mcp import Client, StdioServerParameters
from mcp.types import TextContent


async def main():
    # Tell the client how to start our MCP server.
    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_integration.server"],
    )

    # Connect to the server using stdio.
    async with Client(server_parameters) as client:
        print("Connected to MCP Server!")

        # Discover the tools provided by the server.
        tools_result = await client.list_tools()

        print("\nAvailable tools:")

        for tool in tools_result.tools:
            print(f"- {tool.name}: {tool.description}")

        # Call a tool through the MCP protocol.
        result = await client.call_tool(
            "add_numbers",
            {"a": 25, "b": 17},
        )

        print("\nCalling add_numbers(25, 17):")

        if result.is_error:
            print("Tool execution failed.")
        else:
            for item in result.content:
                if isinstance(item, TextContent):
                    print("Result:", item.text)


if __name__ == "__main__":
    asyncio.run(main())
