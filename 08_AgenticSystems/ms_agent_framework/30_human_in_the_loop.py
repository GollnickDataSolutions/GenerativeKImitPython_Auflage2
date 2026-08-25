#%% packages
import asyncio
import os
import random
from typing import Annotated

from dotenv import load_dotenv
from pydantic import Field

from agent_framework import Agent, Message, tool
from agent_framework.openai import OpenAIChatClient
load_dotenv()

#%% the chat client
chat_client = OpenAIChatClient(
    model="gpt-5.6-luna",
    api_key=os.environ.get("OPENAI_API_KEY"),
)

#%% select a random secret word
WORD_LIST = ["hafen", "traum", "wolke", "regen", "kerze",
             "brief", "stern", "blume", "vogel", "insel"]
MAX_FAILS = 7

secret_word = random.choice(WORD_LIST)

#%% the game state lives in Python, not in the prompt
guessed_letters: set[str] = set()
fails = 0

def render_word() -> str:
    return " ".join(letter if letter in guessed_letters else "_" for letter in secret_word)


def is_solved() -> bool:
    return all(letter in guessed_letters for letter in secret_word)


#%% the guessing tool - every single call needs human approval
@tool(approval_mode="always_require")
def submit_guess(
    letter: Annotated[str, Field(description="Ein einzelner Buchstabe.")],
) -> str:
    """Rät einen Buchstaben und liefert den neuen Spielstand zurück."""
    global fails

    letter = letter.strip().lower()[:1]
    if letter in guessed_letters:
        return f"'{letter}' wurde schon geraten. {render_word()} | Fehler: {fails}/{MAX_FAILS}"

    guessed_letters.add(letter)
    if letter not in secret_word:
        fails += 1

    if is_solved():
        return f"Gewonnen! Das Wort war '{secret_word}'."
    if fails >= MAX_FAILS:
        return f"Verloren! Das Wort war '{secret_word}'."
    return f"{render_word()} | Fehler: {fails}/{MAX_FAILS}"


#%% the guessing agent
hangman_player = Agent(
    client=chat_client,
    name="hangman_player",
    instructions=f"""
    Du spielst Hangman und rätst ein deutsches Wort mit {len(secret_word)} Buchstaben.
    Rate immer nur einen Buchstaben pro Aufruf von submit_guess.
    Beginne mit häufigen Buchstaben (e, n, r, s, t, a) und leite aus dem
    zurückgegebenen Muster ab, welcher Buchstabe als nächstes sinnvoll ist.
    Lehnt der Mensch einen Buchstaben ab, wähle einen anderen.
    Sobald das Tool 'Gewonnen!' oder 'Verloren!' meldet, hörst du auf
    und fasst das Spiel in einem Satz zusammen.
    """,
    tools=[submit_guess],
)


#%% function to play the game
async def play() -> str:
    # the session is required, otherwise the resumed run loses the pending tool call
    session = hangman_player.create_session()
    response = await hangman_player.run("Starte das Spiel.", session=session)

    # a run returns as soon as approvals are pending, it does not block on input
    while response.user_input_requests:
        approval_responses = []
        for request in response.user_input_requests:
            letter = request.function_call.parse_arguments().get("letter")
            print(f"\nStand: {render_word()} | Fehler: {fails}/{MAX_FAILS}")
            print(f"Der Agent möchte '{letter}' raten.")
            approved = input("Freigeben? [j/n] ").strip().lower().startswith("j")
            approval_responses.append(request.to_function_approval_response(approved=approved))
        response = await hangman_player.run(Message("user", approval_responses), session=session)

    return response.text


#%% start the game
summary = asyncio.run(play())
print(f"\n{summary}")

# %%
