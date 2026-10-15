import json

TASKS_FILE = "data/tasks.json"


def load_tasks() -> list:
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def create_task(title: str) -> str:
    tasks = load_tasks()

    next_id = max(
        (task["id"] for task in tasks),
        default=0,
    ) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "completed": False,
    }

    tasks.append(new_task)

    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            tasks,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return "Task created successfully."


def list_tasks() -> list:
    return load_tasks()


def complete_task(task_id: int) -> str:
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True

            with open(TASKS_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    tasks,
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            return "Task completed successfully."

    return "Task not found."


create_task_tool = {
    "type": "function",
    "name": "create_task",
    "description": "Create a new task for the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the task",
            }
        },
        "required": ["title"],
        "additionalProperties": False,
    },
}


list_tasks_tool = {
    "type": "function",
    "name": "list_tasks",
    "description": "List all saved tasks.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
}


complete_task_tool = {
    "type": "function",
    "name": "complete_task",
    "description": "Mark a task as completed using its task ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "The ID of the task to complete",
            }
        },
        "required": ["task_id"],
        "additionalProperties": False,
    },
}


TOOLS = {
    "create_task": create_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
}


TOOL_SCHEMAS = [
    create_task_tool,
    list_tasks_tool,
    complete_task_tool,
]