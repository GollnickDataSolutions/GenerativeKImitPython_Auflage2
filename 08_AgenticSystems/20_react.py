#%% packages
from langchain_openrouter import ChatOpenRouter
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

#%% Create the agent
memory = InMemorySaver()
model = ChatOpenRouter(model="google/gemini-2.5-flash-lite")
search = TavilySearch(max_results=2)
tools = [search]
agent_executor = create_agent(model=model,
                              tools=tools,
                              checkpointer=memory,
                              system_prompt="Du bist ein hilfreicher Assistent, der Fragen beantworten kann. Antworte kurz und präzise in deutscher Sprache.")

#%% Use the agent
config = {"configurable": {"thread_id": "abcd123"}}

#%%
agent_executor.invoke(
    {"messages": [("user", "Mein Name ist Bert Gollnick, ich bin Trainer und Data Scientist. Ich lebe in Hamburg")]}, config
)

#%% function for extracting the last message from the memory
def get_last_message(memory, config):
    return memory.get_tuple(config=config).checkpoint['channel_values']['messages'][-1].content

#%% check whether the model can remember me
agent_executor.invoke(
    {"messages": [("user", "Wie heiße ich und in welchem Land lebe ich?")]}, config
)
get_last_message(memory, config)
#%% check if it is possible to find me in the internet
agent_executor.invoke(
    {"messages": [("user", "Suche im Internet nach öffentlichen Informationen über die genannte Person.")]},
    config
)
get_last_message(memory, config)

# %% all checkpoints of this thread
list(memory.list(config=config))

# %% extract the last message from the memory
get_last_message(memory, config)

#%% 
from pyperclip import copy
copy(get_last_message(memory, config))
# %%