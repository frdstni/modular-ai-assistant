
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from core.config import MODEL_NAME, OPENROUTER_API_KEY
from tools.langchain_registry import LANGCHAIN_TOOLS

# 1. Create the model
model = ChatOpenRouter(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    temperature=0,
    timeout=120000,
    max_retries=0,
    max_tokens=500,
)


# 2. Give the model access to our tools
model_with_tools = model.bind_tools(LANGCHAIN_TOOLS)


# 3. Create the assistant node
def assistant_node(state: MessagesState):
    response = model_with_tools.invoke(state["messages"])

    return {"messages": [response]}


# 4. Create the graph builder
builder = StateGraph(MessagesState)


# 5. Register the nodes
builder.add_node("assistant", assistant_node)
builder.add_node(
    "tools",
    ToolNode(
        LANGCHAIN_TOOLS,
        handle_tool_errors=True,
    ),
)


# 6. Define the execution flow
builder.add_edge(START, "assistant")

builder.add_conditional_edges(
    "assistant",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "assistant")


# 7. Add an in-memory checkpointer
checkpointer = InMemorySaver()


# 8. Compile the graph
graph = builder.compile(checkpointer=checkpointer)


def main():
    print("Modular AI Assistant — LangGraph")
    print("Type 'exit' to quit.")

    # Keep the same conversation thread during this session.
    config = {
        "configurable": {
            "thread_id": "local-cli-session",
        }
    }

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            result = graph.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ]
                },
                config=config,
            )

            print("Assistant:", result["messages"][-1].content)

        except Exception as error:# noqa: BLE001
            print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
