#%% packages
import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv
load_dotenv()

MODEL = "gpt-5.6-luna"

#%% define the agents
# handoff_description sagt dem Triage-Agenten, wann er an diesen Agenten uebergibt
english_agent = Agent(
    name="English Agent",
    instructions="You are a helpful agent and only speak in English.",
    handoff_description="Handles requests written in English.",
    model=MODEL,
)

german_agent = Agent(
    name="German Agent",
    instructions="Du bist ein hilfreicher Agent und sprichst ausschließlich Deutsch.",
    handoff_description="Beantwortet Anfragen, die auf Deutsch gestellt werden.",
    model=MODEL,
)

#%% triage agent
phone_operator_agent = Agent(
    name="Triage Agent",
    instructions="You are a helpful agent that can handoff to the appropriate agent based on the user's language.",
    handoffs=[english_agent, german_agent],
    model=MODEL,
)

#%% run the request
prompt = "Ich brauche Hilfe mit meiner Buchung."
# prompt = "Excuse me, I need help with my booking."
response = asyncio.run(
    Runner.run(phone_operator_agent, input=prompt)
)

# %% the answer of the agent that took over
print(response.final_output)

# %% which agent answered in the end?
print(response.last_agent.name)

# %% check all raw responses
response.raw_responses

# %%
