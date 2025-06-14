from google import genai
import os
import json
import requests

from .prompt import SYSTEM_PROMPT
from .models import AgentResponse, UserQuestion, ConversationHistory, Tool, Tools
from .clean_response import clean_response

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def run():
    user_input = ""

    conversation_history = ConversationHistory(interactions=[])
    user_input = input("Enter your prompt: ")

    while user_input.lower() != "exit" or user_input.lower() != "clear":
        user_question = UserQuestion(question=user_input)
        raw_tools = requests.get('http://localhost:8000/api/get_tools').json()
        print(f"raw_tools: {raw_tools}")
        validated_tools = [Tool.model_validate_json(tool) for tool in raw_tools]
        tools_json = [tool.model_dump_json() for tool in validated_tools]

        prompt = f"""
{SYSTEM_PROMPT}\n\n
<tools>\n{tools_json}\n</tools>\n\n
<conversation_history>\n{conversation_history.model_dump_json()}\n</conversation_history>\n\n
<user_question>\n{user_question.model_dump_json()}\n</user_question>\n\n
"""

        print(
            "########## LLM PROMPT:\n\n"
            rf"{prompt}"
            "\n########## END OF LLM PROMPT\n"
        )

        conversation_history.interactions.append(user_question)

        raw_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        ).text

        print(
            "########## LLM RAW RESPONSE:\n\n"
            rf"{raw_response}"
            "\n########## END OF LLM RAW RESPONSE\n"
        )

        response = json.loads(clean_response(raw_response))

        print(
            "########## LLM DESERIALIZED RESPONSE:\n\n"
            rf"{response}"
            "\n########## END OF LLM DESERIALIZED RESPONSE\n"
        )

        agent_response = AgentResponse.model_validate(response)

        print(agent_response.model_dump_json())

        conversation_history.interactions.append(agent_response)

        user_input = input("Enter your prompt: ")


if __name__ == "__main__":
    run()
