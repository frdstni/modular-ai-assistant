import os

from dotenv import load_dotenv

load_dotenv()


PROJECT_NAME = os.getenv("PROJECT_NAME", "Modular AI Assistant")

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.5")

OPENROUTER_API_KEY= os.getenv("OPENROUTER_API_KEY")
