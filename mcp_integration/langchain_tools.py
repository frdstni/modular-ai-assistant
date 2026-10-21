
import json
from typing import Any

from langchain_core.tools import StructuredTool
from mcp.types import TextContent
from pydantic import Field, create_model


def get_python_type(json_type: str):
    """Convert a JSON Schema type to a Python type."""
    types = {
        "string": str,
        "number": float,
        "integer": int,
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    return types.get(json_type, Any)


def create_args_schema(mcp_tool):
    """Build a Pydantic schema from an MCP tool schema."""
    input_schema = getattr(mcp_tool, "inputSchema", None)

    if input_schema is None:
        input_schema = getattr(mcp_tool, "input_schema", {})

    if hasattr(input_schema, "model_dump"):
        input_schema = input_schema.model_dump(by_alias=True)

    properties = input_schema.get("properties", {})
    required_fields = set(input_schema.get("required", []))

    fields = {}

    for name, details in properties.items():
        python_type = get_python_type(details.get("type"))
        description = details.get("description", "")

        if name in required_fields:
            fields[name] = (
                python_type,
                Field(..., description=description),
            )
        else:
            fields[name] = (
             python_type | None,
             Field(default=None, description=description),
       )

    model_name = "".join(
        part.capitalize()
        for part in mcp_tool.name.split("_")
    ) + "Input"

    return create_model(model_name, **fields)


def get_result_text(result) -> str:
    """Extract readable output from an MCP tool result."""
    text_parts = [
        item.text
        for item in result.content
        if isinstance(item, TextContent)
    ]

    if text_parts:
        return "\n".join(text_parts)

    structured_content = getattr(
        result,
        "structuredContent",
        None,
    )

    if structured_content is None:
        structured_content = getattr(
            result,
            "structured_content",
            None,
        )

    if structured_content is not None:
        return json.dumps(
            structured_content,
            ensure_ascii=False,
        )

    return str(result)


async def load_mcp_tools(client):
    """Discover MCP tools and convert them to LangChain tools."""
    response = await client.list_tools()

    langchain_tools = []

    for mcp_tool in response.tools:

        def create_tool_function(tool_name):
            async def call_mcp_tool(**arguments):
                print(f"[MCP] Calling tool: {tool_name}")

                result = await client.call_tool(
                    tool_name,
                    arguments,
                )

                output = get_result_text(result)

                if result.is_error:
                    raise RuntimeError(
                        output or f"MCP tool failed: {tool_name}"
                    )

                return output

            return call_mcp_tool

        langchain_tool = StructuredTool(
            name=mcp_tool.name,
            description=mcp_tool.description or mcp_tool.name,
            args_schema=create_args_schema(mcp_tool),
            coroutine=create_tool_function(mcp_tool.name),
        )

        langchain_tools.append(langchain_tool)

    return langchain_tools
