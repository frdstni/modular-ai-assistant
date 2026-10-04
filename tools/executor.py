import json

from tools.registry import TOOLS


def execute_tool(item):
    tool_function = TOOLS.get(item.name)

    if tool_function is None:
        return None, f"Unknown tool: {item.name}"

    try:
        arguments = json.loads(item.arguments)
        result = tool_function(**arguments)

        return result, None

    except (json.JSONDecodeError, TypeError, ZeroDivisionError) as error:
        return None, str(error)