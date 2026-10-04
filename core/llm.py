from openai import OpenAI

from core.config import GROQ_API_KEY, MODEL_NAME

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def ask_model(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    return response.output_text