from langchain_core.tools import tool

from tools.calculator import (
    add as calculator_add,
)
from tools.calculator import (
    divide as calculator_divide,
)
from tools.calculator import (
    multiply as calculator_multiply,
)
from tools.notes import (
    read_notes as read_notes_function,
)
from tools.notes import (
    save_note as save_note_function,
)
from tools.tasks import (
    complete_task as complete_task_function,
)
from tools.tasks import (
    create_task as create_task_function,
)
from tools.tasks import (
    list_tasks as list_tasks_function,
)

# -------------------------
# Calculator Tools
# -------------------------

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return calculator_add(a, b)


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return calculator_multiply(a, b)


@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
    return calculator_divide(a, b)


# -------------------------
# Notes Tools
# -------------------------

@tool
def save_note(text: str) -> str:
    """Save a note for the user."""
    return save_note_function(text)


@tool
def read_notes() -> str:
    """Read all saved notes."""
    return str(read_notes_function())


# -------------------------
# Tasks Tools
# -------------------------

@tool
def create_task(title: str) -> str:
    """Create a new task for the user."""
    return create_task_function(title)


@tool
def list_tasks() -> str:
    """List all saved tasks."""
    return str(list_tasks_function())


@tool
def complete_task(task_id: int) -> str:
    """Mark a task as completed using its task ID."""
    return complete_task_function(task_id)