
import asyncio
import sys

from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from mcp import Client, StdioServerParameters

from core.config import MODEL_NAME, OPENROUTER_API_KEY
from mcp_integration.langchain_tools import load_mcp_tools


def build_graph(tools):
    """Build a LangGraph workflow using MCP tools."""

    model = ChatOpenRouter(
        model=MODEL_NAME,
        api_key=OPENROUTER_API_KEY,
        temperature=0,
        timeout=120000,
        max_retries=0,
        max_tokens=500,
    )

    model_with_tools = model.bind_tools(tools)

    async def assistant_node(state: MessagesState):
        response = await model_with_tools.ainvoke(
            state["messages"]
        )

        return {"messages": [response]}

    builder = StateGraph(MessagesState)

    builder.add_node("assistant", assistant_node)

    builder.add_node(
        "tools",
        ToolNode(
            tools,
            handle_tool_errors=True,
        ),
    )

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

    checkpointer = InMemorySaver()

    return builder.compile(checkpointer=checkpointer)


async def main():
    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_integration.server"],
    )

    async with Client(server_parameters) as client:
        print("Connected to MCP Server!")

        tools = await load_mcp_tools(client)

        print("\nTools available to LangGraph:")

        for tool in tools:
            print(f"- {tool.name}")

        graph = build_graph(tools)

        config = {
            "configurable": {
                "thread_id": "mcp-cli-session",
            }
        }

        print("\nModular AI Assistant — MCP + LangGraph")
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
