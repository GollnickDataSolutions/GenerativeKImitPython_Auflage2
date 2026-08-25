#%% Packages
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from dotenv import load_dotenv
from rich.markdown import Markdown
from rich.console import Console
console = Console()
load_dotenv()

#%% Prepare LLM
MODEL_NAME = 'gpt-5.5'
llm = ChatOpenAI(model=MODEL_NAME)
# %% Session history
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

#%% Begin the story
initial_prompt = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein kreativer Erzähler. Basierend auf dem folgenden Kontext und der Wahl des Spielers, fahre die Geschichte fort und biete drei neue Wahlen für den Spieler an. Halte die Geschichte extrem kurz und konzise. Erstelle eine Öffnungsszene für eine Abenteuerstory {place} und biete drei initiale Wahlen für den Spieler an.")
])

context_chain = initial_prompt | llm

config = {"configurable": {"session_id": "03"}}

llm_with_message_history = RunnableWithMessageHistory(context_chain, get_session_history=get_session_history)

context = llm_with_message_history.invoke({"place": "ein dunkler Wald"}, config=config)

# render opening scene as markdown output
console.print(Markdown(context.content))

#%% Function to process player's choice
def process_player_choice(choice):
    response = llm_with_message_history.invoke(
        [("user", f"Fahre die Geschichte fort basierend auf der Wahl des Spielers: {choice}"),
        ("system", "Biete drei neue Wahlmöglichkeiten für den Spieler an.")]
        , config=config)
    return response

# %% Game loop
while True:
    # get player's choice
    player_choice = input("Triff deine Wahl oder 'quit' um das Spiel zu beenden)")
    console.print(f"Du hast gewählt: {player_choice}")
    if player_choice.lower() == "quit":
        break
    # continue the story
    context = process_player_choice(player_choice)
    console.print(Markdown(context.content))
# %%
console.print(Markdown(context.content))
