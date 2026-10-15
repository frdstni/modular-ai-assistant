from openai import OpenAI

from core.config import OPENROUTER_API_KEY, MODEL_NAME
from tools.registry import TOOL_SCHEMAS

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
     base_url="https://openrouter.ai/api/v1",
)


def ask_model(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    return response.output_text

def ask_model_with_tools(prompt: str):
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
        tools=TOOL_SCHEMAS,
         tool_choice="auto",
    )

    return response