from google import genai
import os
import json
import requests

from pydantic import ValidationError

from .prompt import SYSTEM_PROMPT
from .models import (
    AgentResponse,
    UserQuestion,
    ConversationHistory,
    AgentTool,
    ToolCall,
    ToolCompletion,
)
from .api import ToolRepresentation
from .clean_response import clean_response

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def run():
    user_input = ""

    conversation_history = ConversationHistory(interactions=[])
    user_input = input("User Question: ")

    while user_input.lower() != "exit" or user_input.lower() != "clear":
        user_question = UserQuestion(question=user_input)
        raw_tools = requests.get("http://localhost:8000/api/get_tools").json()
        tools_representation = [
            ToolRepresentation.model_validate_json(tool) for tool in raw_tools
        ]
        agent_tools = [AgentTool.model_validate_json(tool) for tool in raw_tools]
        agent_tools_json = [tool.model_dump_json() for tool in agent_tools]

        prompt = f"""
{SYSTEM_PROMPT}\n\n
<tools>\n{agent_tools_json}\n</tools>\n\n
<conversation_history>\n{conversation_history.model_dump_json()}\n</conversation_history>\n\n
<user_question>\n{user_question.model_dump_json()}\n</user_question>\n\n
"""

        conversation_history.interactions.append(user_question)

        print(f"Prompt: {prompt}")

        raw_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        ).text

        response = json.loads(clean_response(raw_response))

        tool_call = None

        try:
            print(f"Raw Response: {response}")
            tool_call = ToolCall.model_validate(response)
        except ValidationError:
            ...

        if tool_call:
            chosen_tool = [
                tool
                for tool in tools_representation
                if tool.tool_name == tool_call.tool_name
            ]
            url = f"{chosen_tool[0].url}{chosen_tool[0].tool_name}/"
            tool_response = requests.post(
                url,
                json=tool_call.parameters,
            ).json()

            print(f"Tool Response: {tool_response}")

            conversation_history.interactions.append(
                ToolCompletion(
                    tool_called=tool_call.tool_name,
                    parameters=tool_call.parameters,
                    returned_value=tool_response,
                )
            )

            tool_call = None

            continue

        agent_response = AgentResponse.model_validate(response)

        conversation_history.interactions.append(agent_response)

        print(f"AI Agent: {agent_response.response}")

        user_input = input("User Question: ")


if __name__ == "__main__":
    run()
