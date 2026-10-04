from core.llm import ask_model_with_tools
from tools.executor import execute_tool


def main():
    user_input = input("You: ")

    input_items = [
        {
            "role": "user",
            "content": user_input,
        }
    ]

    response = ask_model_with_tools(input_items)

    input_items.extend(response.output)

    for item in response.output:
        if item.type == "function_call":
            result, error = execute_tool(item)

            if error:
                print(f"Tool error: {error}")
                return

            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": str(result),
                }
            )

            final_response = ask_model_with_tools(input_items)

            print(f"Assistant: {final_response.output_text}")
            return

    print(f"Assistant: {response.output_text}")


if __name__ == "__main__":
    main()