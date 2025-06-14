from google import genai
import os
import json

from .prompt import SYSTEM_PROMPT
from .models import AgentResponse, UserQuestion, ConversationHistory
from .clean_response import clean_response

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def run():
    user_input = ""

    conversation_history = ConversationHistory(interactions=[])
    user_input = input("Enter your prompt: ")

    while user_input.lower() != "exit":
        user_question = UserQuestion(question=user_input)

        prompt = f"""
{SYSTEM_PROMPT}\n\n
<conversation_history>\n{conversation_history.model_dump_json()}\n</conversation_history>\n\n
<user_question>\n{user_question.model_dump_json()}\n</user_question>\n\n
"""

        conversation_history.interactions.append(user_question)

        print(prompt)

        raw_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        ).text

        print(
            "########## LLM RAW RESPONSE:\n\n"
            fr"{raw_response}"
            "\n\n########## END OF LLM RAW RESPONSE"
        )

        response = json.loads(clean_response(raw_response))

        print(
            "########## LLM PARSED RESPONSE:\n\n"
            fr"{response}"
            "\n\n########## END OF LLM PARSED RESPONSE"
        )

        agent_response = AgentResponse.model_validate(response)

        print(agent_response.model_dump_json())

        conversation_history.interactions.append(agent_response)

        user_input = input("Enter your prompt: ")


if __name__ == "__main__":
    run()
