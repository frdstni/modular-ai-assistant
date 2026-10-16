from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter

from core.config import MODEL_NAME, OPENROUTER_API_KEY
from tools.langchain_registry import LANGCHAIN_TOOLS

# Create the model
model = ChatOpenRouter(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    temperature=0,
    timeout=120000,
    max_retries=0,
    max_tokens=500,
)


# Create the agent
agent = create_agent(
    model=model,
    tools=LANGCHAIN_TOOLS,
    system_prompt="You are a helpful assistant.",
)


def main():
    user_input = input("You: ")

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        }
    )

    print("Assistant:", result["messages"][-1].content)


if __name__ == "__main__":
    main()