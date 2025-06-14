from pydantic import BaseModel, TypeAdapter

class ToolCall(BaseModel):
    name: str
    parameters: dict[str, str]


class Tool(BaseModel):
    name: str
    function_signature: str
    description: str
    parameters_description: dict[str, str]

Tools = TypeAdapter[list[Tool]]


class ToolCompletion(BaseModel):
    tool_called: str
    parameters: dict[str, str]
    return_value: str


class UserQuestion(BaseModel):
    question: str


class AgentResponse(BaseModel):
    response: str


class ConversationHistory(BaseModel):
    interactions: list[UserQuestion | ToolCompletion | AgentResponse]