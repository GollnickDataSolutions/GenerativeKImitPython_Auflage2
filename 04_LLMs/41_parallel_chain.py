#%% packages
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

#%% Model Instance
MODEL_NAME = 'gpt-5.5'
llm = ChatOpenAI(model=MODEL_NAME)

#%% Prepare Prompts
# example: style variations (friendly, polite) vs. (savage, angry)
polite_prompt = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein hilfreicher Assistent. Antworte in einer freundlichen und freundlichen Art."),
    ("human", "{topic}")
])

savage_prompt = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein hilfreicher Assistent. Antworte in einer wilden und wütenden Art."),
    ("human", "{topic}")
])

#%% Prepare Chains
polite_chain = polite_prompt | llm | StrOutputParser()
savage_chain = savage_prompt | llm | StrOutputParser()


# %% Runnable Parallel
map_chain = RunnableParallel(
    polite=polite_chain,
    savage=savage_chain
)

# %% Invoke
topic = "Was ist der Sinn des Lebens?"
result = map_chain.invoke({"topic": topic})
# %% Print
from pprint import pprint
pprint(result)
# %%
result