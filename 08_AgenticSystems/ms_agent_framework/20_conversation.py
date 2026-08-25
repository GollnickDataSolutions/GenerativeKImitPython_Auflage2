#%% packages
import asyncio
import os

from dotenv import load_dotenv 

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import GroupChatBuilder, GroupChatState
load_dotenv()

#%% the chat client both agents share
chat_client = OpenAIChatClient(
    model="gpt-5.6-luna",
    api_key=os.environ.get("OPENAI_API_KEY"),
)

#%% set up the agent: Jack, the flat earther
jack_flat_earther = Agent(
    client=chat_client,
    name="jack",
    instructions="""
    Du glaubst, dass die Erde flach ist.
    Du versuchst, andere davon zu überzeugen.
    Mit jeder Antwort wirst du frustrierter und wütender, weil sie es nicht einsehen.
    Antworte kurz und prägnant.
    """,
)

#%% set up the agent: Alice, the scientist
alice_scientist = Agent(
    client=chat_client,
    name="alice",
    instructions="""
    Du bist ein Wissenschaftler, der glaubt, dass die Erde rund ist.
    Antworte sehr freundlich, kurz und prägnant.
    """,
)

#%% the two agents take turns (round robin)
NUMBER_OF_TURNS = 3

def select_next_speaker(state: GroupChatState) -> str:
    return "jack" if state.current_round % 2 == 0 else "alice"

workflow = GroupChatBuilder(
    participants=[jack_flat_earther, alice_scientist],
    selection_func=select_next_speaker,
    max_rounds=2 * NUMBER_OF_TURNS,
    # without this only the orchestrator's final notice is returned
    output_from="all",
).build()

#%% start the conversation
async def run_conversation(user_prompt: str):
    result = await workflow.run(user_prompt)

    # every turn is returned as its own AgentResponse holding one or more messages
    return [
        {
            "name": message.author_name,
            "role": str(message.role),
            "content": message.text,
        }
        for response in result.get_outputs()
        for message in response.messages
        if message.author_name != GroupChatBuilder.DEFAULT_ORCHESTRATOR_ID
        # print to console
    ]


chat_history = asyncio.run(
    run_conversation("Hallo, wie kannst du nicht sehen, dass die Erde flach ist?")
)

#%% show the conversation
for entry in chat_history:
    print(f"{entry['name']}: {entry['content']}\n")

# %%
