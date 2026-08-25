
#%% packages
import asyncio
import os
from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import GroupChatBuilder, GroupChatState
load_dotenv()
#%% load the environment variables
import streamlit as st

#%% the chat client both agents share
chat_client = OpenAIChatClient(
    model="gpt-5.6-luna",
    api_key=os.environ.get("OPENAI_API_KEY"),
)

#%% the styles the user can choose from
STYLES = {
    "Freundlich": "freundliche",
    "Neutral": "sachliche",
    "Unfreundlich": "unfreundliche",
}

st.title("Kontroverse Debatte")

prompt = st.chat_input("Gib ein Thema für die Debatte ein:")
if prompt:
    st.header(f"Thema: {prompt}")

with st.expander("Einstellungen für das Gespräch"):
    number_of_turns = st.slider("Anzahl der Runden", min_value=1, max_value=10, value=1)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Stil von Person A")
        style_a = st.radio(
            "Stil der ersten Person wählen:",
            list(STYLES.keys()),
            key="style_a"
        )

    with col2:
        st.subheader("Stil von Person B")
        style_b = st.radio(
            "Stil der zweiten Person wählen:",
            list(STYLES.keys()),
            key="style_b"
        )


#%% start the conversation
async def run_conversation(user_prompt: str, number_of_turns: int):
    # set up the agent: the believer
    person_a = Agent(
        client=chat_client,
        name="user",
        instructions=f"""
        Du bist eine Person, die daran glaubt, dass {user_prompt}.
        Du versuchst, andere davon zu überzeugen.
        Du antwortest auf {STYLES[style_a]} Weise.
        Antworte auf Deutsch, sehr kurz und prägnant.
        """,
    )

    # set up the agent: the sceptic
    person_b = Agent(
        client=chat_client,
        name="ai",
        instructions=f"""
        Du bist eine Person, die das Gegenteil von {user_prompt} glaubt.
        Du antwortest auf {STYLES[style_b]} Weise.
        Antworte auf Deutsch, sehr kurz und prägnant.
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

    result = await workflow.run(user_prompt)

    # every turn is returned as its own AgentResponse holding one or more messages
    return [
        {
            "name": message.author_name,
            "content": message.text,
        }
        for response in result.get_outputs()
        for message in response.messages
        if message.author_name != GroupChatBuilder.DEFAULT_ORCHESTRATOR_ID
    ]


#%% show the conversation
if prompt:
    with st.spinner("Die Agenten diskutieren ..."):
        messages = asyncio.run(
            run_conversation(user_prompt=prompt, number_of_turns=number_of_turns)
        )

    for message in messages:
        name = message["name"]
        if name == "user":
            with st.container():
                col1, col2 = st.columns([3, 7])
                with col2:
                    with st.chat_message(name=name):
                        st.write(message["content"])
        else:
            with st.container():
                col1, col2 = st.columns([7, 3])
                with col1:
                    with st.chat_message(name=name):
                        st.write(message["content"])
