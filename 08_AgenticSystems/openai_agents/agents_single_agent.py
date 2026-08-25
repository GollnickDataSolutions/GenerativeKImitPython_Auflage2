#%% packages
import asyncio

from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

# %% define the agent
# ohne "model" verwendet das SDK sein Standardmodell (aktuell gpt-5.4-mini)
agent = Agent(
    name="my_first_agent",
    instructions="Du bist ein hilfreicher Assistent, der Fragen beantworten und bei Aufgaben helfen kann.",
    model="gpt-5.6-luna",
)

# %% run the agent
response = asyncio.run(
    Runner.run(agent, input="Hallo, was ist OpenAI Agents?")
)

# %% model output
print(response.final_output)

# %%
