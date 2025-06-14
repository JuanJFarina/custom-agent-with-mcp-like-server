from fastapi import APIRouter
from custom_agent_with_mcp_like_server.api.tools import reduce_to_numbers as tool
from .models import StringInput, ToolsRepresentations
import json
from pathlib import Path

router = APIRouter()

tools_path = Path(f"{Path(__file__).resolve().parent}/tools.json")


@router.get("/get_tools")
def get_tools():
    with tools_path.open(encoding="utf-8") as tools_file:
        tools = json.load(tools_file)
    validated_tools = ToolsRepresentations.validate_python(tools)
    return [validated_tool.model_dump_json() for validated_tool in validated_tools]


@router.post("/reduce_to_numbers/")
def reduce_to_numbers(string: StringInput) -> str:
    return tool(string.content)
