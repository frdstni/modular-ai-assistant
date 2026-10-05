import json

NOTES_FILE = "data/notes.json"


def load_notes() -> list:
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_note(text: str) -> str:
    notes = load_notes()

    next_id = max(
        (note["id"] for note in notes),
        default=0,
    ) + 1

    new_note = {
        "id": next_id,
        "text": text,
    }

    notes.append(new_note)

    with open(NOTES_FILE, "w", encoding="utf-8") as file:
        json.dump(
            notes,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return "Note saved successfully."


def read_notes() -> list:
    return load_notes()


save_note_tool = {
    "type": "function",
    "name": "save_note",
    "description": "Save a note for the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The note text to save",
            }
        },
        "required": ["text"],
        "additionalProperties": False,
    },
}


read_notes_tool = {
    "type": "function",
    "name": "read_notes",
    "description": "Read all saved notes.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
}


TOOLS = {
    "save_note": save_note,
    "read_notes": read_notes,
}


TOOL_SCHEMAS = [
    save_note_tool,
    read_notes_tool,
]