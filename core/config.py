import os
from dotenv import load_dotenv


load_dotenv()


PROJECT_NAME = os.getenv(
    "PROJECT_NAME",
    "Modular AI Assistant"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "default-model"
)