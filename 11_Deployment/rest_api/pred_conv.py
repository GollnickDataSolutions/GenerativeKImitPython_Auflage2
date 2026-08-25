#%% packages
import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import GroupChatBuilder, GroupChatState

#%% load the environment variables
load_dotenv()

#%% define the function to predict
async def predict_conversation_async(user_prompt: str, number_of_turns: int):
    chat_client = OpenAIChatClient(
        model="gpt-5.6-luna",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # set up the agent: the believer
    person_a = Agent(
        client=chat_client,
        name="user",
        instructions=f"""
        Du bist eine Person, die daran glaubt, dass {user_prompt}.
        Du versuchst, andere davon zu überzeugen.
        Du antwortest auf freundliche Weise.
        Antworte sehr kurz und prägnant.
        """,
    )

    # set up the agent: the sceptic
    person_b = Agent(
        client=chat_client,
        name="ai",
        instructions=f"""
        Du bist eine Person, die das Gegenteil von {user_prompt} glaubt.
        Du antwortest auf sachliche Weise.
        Antworte sehr kurz und prägnant.
        """,
    )

    # the two agents take turns (round robin)
    def select_next_speaker(state: GroupChatState) -> str:
        return "user" if state.current_round % 2 == 0 else "ai"

    workflow = GroupChatBuilder(
        participants=[person_a, person_b],
        selection_func=select_next_speaker,
        max_rounds=2 * number_of_turns,
        # without this only the orchestrator's final notice is returned
        output_from="all",
    ).build()

    #  start the conversation
    result = await workflow.run(user_prompt)

    # every turn is returned as its own AgentResponse holding one or more messages
    messages = [
        {
            "name": message.author_name,
            "role": str(message.role),
            "content": message.text,
        }
        for response in result.get_outputs()
        for message in response.messages
        if message.author_name != GroupChatBuilder.DEFAULT_ORCHESTRATOR_ID
    ]
    return messages


def predict_conversation(user_prompt: str, number_of_turns: int):
    return asyncio.run(
        predict_conversation_async(
            user_prompt=user_prompt,
            number_of_turns=number_of_turns,
        )
    )
