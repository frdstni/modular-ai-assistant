from tools.calculator import TOOL_SCHEMAS as CALCULATOR_SCHEMAS
from tools.calculator import TOOLS as CALCULATOR_TOOLS
from tools.notes import TOOL_SCHEMAS as NOTES_SCHEMAS
from tools.notes import TOOLS as NOTES_TOOLS
from tools.tasks import TOOL_SCHEMAS as TASKS_SCHEMAS
from tools.tasks import TOOLS as TASKS_TOOLS

TOOLS = {
    **CALCULATOR_TOOLS,
    **NOTES_TOOLS,
    **TASKS_TOOLS,
}


TOOL_SCHEMAS = [
    *CALCULATOR_SCHEMAS,
    *NOTES_SCHEMAS,
    *TASKS_SCHEMAS,
]