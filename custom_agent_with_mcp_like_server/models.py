from pydantic import BaseModel, TypeAdapter


class Tool(BaseModel):
    name: str
    description: str


Tools = TypeAdapter[list[Tool]]


class ToolCall(BaseModel):
    name: str
    parameters: dict[str, str]


class ToolCompletion(BaseModel):
    tool_called: str
    parameters: dict[str, str]
    returned_value: str


class UserQuestion(BaseModel):
    question: str


class AgentResponse(BaseModel):
    response: str


class ConversationHistory(BaseModel):
    interactions: list[UserQuestion | ToolCompletion | AgentResponse]
