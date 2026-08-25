#%% packages
from langsmith import Client
from langchain_openrouter import ChatOpenRouter
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

#%% fetch prompt
client = Client()
prompt = client.pull_prompt("hardkothari/prompt-maker", dangerously_pull_public_prompt=True)

#%% get input variables
prompt.input_variables
#%% show model parameters
MODEL_NAME = 'google/gemini-3.1-flash-lite'
model = ChatOpenRouter(model=MODEL_NAME)
print("Model parameters:")
print("Model name:", model.model)
print("Temperature:", model.temperature)

# %% model
model = ChatOpenRouter(model=MODEL_NAME)

# %% chain
chain = prompt | model | StrOutputParser()

# %% invoke chain
lazy_prompt = "Sommer, Urlaub, Strand"
task = "Shakespeare Gedicht"
improved_prompt = chain.invoke({"lazy_prompt": lazy_prompt, "task": task})
# %%
print(improved_prompt)

# %% run model with improved prompt
res = model.invoke(improved_prompt)
print(res.content)

# %%
res = model.invoke("summer, vacation, beach, Shakespeare poem")
print(res.content)
# %%
