from pydantic import BaseModel, TypeAdapter


class AgentTool(BaseModel):
    tool_name: str
    description: str


Tools = TypeAdapter[list[AgentTool]]


class ToolCall(BaseModel):
    tool_name: str
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
