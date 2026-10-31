

import asyncio
import sys

from langchain_core.messages import SystemMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from mcp import Client, StdioServerParameters

from core.config import MODEL_NAME, OPENROUTER_API_KEY
from mcp_integration.langchain_tools import load_mcp_tools


# 1. Build the LangGraph workflow
def build_graph(tools):

    # Create the model
    model = ChatOpenRouter(
        model=MODEL_NAME,
        api_key=OPENROUTER_API_KEY,
        temperature=0,
        timeout=120000,
        max_retries=0,
        max_tokens=500,
    )

    # Give the model access to MCP tools
    model_with_tools = model.bind_tools(tools)

    # Assistant node
    async def assistant_node(state: MessagesState):

        system_message = SystemMessage(
            content="""
            You are a helpful general-purpose AI assistant.

            Instructions:
            - Answer general questions directly.
            - Use tools when necessary.
            - Use calculator tools for mathematical operations.
            - Use notes tools for saving and reading notes.
            - Use tasks tools for task management.
            - Never claim an action was completed unless the tool confirms it.
            - If a request is outside your capabilities, explain your limitations.
            - Respond in the same language as the user.
            """
        )

        messages = [
            system_message,
            *state["messages"],
        ]

        response = await model_with_tools.ainvoke(messages)

        return {"messages": [response]}

    # Create graph
    builder = StateGraph(MessagesState)

    # Register nodes
    builder.add_node("assistant", assistant_node)

    builder.add_node(
        "tools",
        ToolNode(
            tools,
            handle_tool_errors=True,
        ),
    )

    # Define workflow
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

    # Add in-memory checkpointing
    checkpointer = InMemorySaver()

    return builder.compile(checkpointer=checkpointer)


# 2. Run the assistant
async def main():

    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_integration.server"],
    )

    async with Client(server_parameters) as client:

        print("Connected to MCP Server!")

        # Discover MCP tools
        tools = await load_mcp_tools(client)

        print("\nAvailable tools:")

        for tool in tools:
            print(f"- {tool.name}")

        # Build graph
        graph = build_graph(tools)

        config = {
            "configurable": {
                "thread_id": "mcp-cli-session",
            }
        }

        print("\nModular AI Assistant")
        print("Type 'exit' to quit.")

        while True:

            user_input = await asyncio.to_thread(
                input,
                "\nYou: ",
            )

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            if not user_input.strip():
                continue

            try:
                result = await graph.ainvoke(
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

                print(
                    "Assistant:",
                    result["messages"][-1].content,
                )

            except Exception as error:  # noqa: BLE001
                print(f"An error occurred: {error}")


if __name__ == "__main__":
    asyncio.run(main())

