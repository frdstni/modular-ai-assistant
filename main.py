from core.config import PROJECT_NAME
from core.llm import ask_model


def main():
    print(f"Starting {PROJECT_NAME}")

    user_input = input("You: ")

    response = ask_model(user_input)

    print(f"Assistant: {response}")


if __name__ == "__main__":
    main()
