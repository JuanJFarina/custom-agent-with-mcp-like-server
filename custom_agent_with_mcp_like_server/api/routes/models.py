from pydantic import BaseModel, TypeAdapter
import os


class ToolRepresentation(BaseModel):
    tool_name: str
    description: str
    url: str = f"{os.getenv('BASE_URL', '')}/api/"
    method: str


ToolsRepresentations = TypeAdapter(list[ToolRepresentation])


class StringInput(BaseModel):
    content: str
