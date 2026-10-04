def add(a: float, b: float) -> float:
    return a + b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    return a / b


calculator_tool = {
    "type": "function",
    "name": "add",
    "description": "Add two numbers together.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "The first number",
            },
            "b": {
                "type": "number",
                "description": "The second number",
            },
        },
        "required": ["a", "b"],
        "additionalProperties": False,
    },
}

multiply_tool = {
    "type": "function",
    "name": "multiply",
    "description": "Multiply two numbers.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "The first number",
            },
            "b": {
                "type": "number",
                "description": "The second number",
            },
        },
        "required": ["a", "b"],
        "additionalProperties": False,
    },
}

divide_tool = {
    "type": "function",
    "name": "divide",
    "description": "Divide the first number by the second number.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "The first number",
            },
            "b": {
                "type": "number",
                "description": "The second number",
            },
        },
        "required": ["a", "b"],
        "additionalProperties": False,
    },
}

TOOLS = {
    "add": add,
     "multiply": multiply,
     "divide": divide,
}

TOOL_SCHEMAS = [
    calculator_tool,
    multiply_tool,
     divide_tool,
]