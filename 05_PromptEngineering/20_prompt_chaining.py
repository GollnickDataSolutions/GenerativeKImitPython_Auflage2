#%% packages
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
load_dotenv()


#%%
model = ChatOpenRouter(model_name='openai/gpt-5.6-luna')

#%% first run
messages = [
        ("system", "Du bist ein Autor und schreibst ein Kinderbuch. Antworte kurz und präzise. Ende deine Antwort mit einer spezifischen Frage, die eine neue Richtung für die Geschichte bietet."),
        ("user", "Ein Maus und ein Hund sind beste Freunde."),
    ]
prompt = ChatPromptTemplate.from_messages(messages)
chain = prompt | model
output = chain.invoke({})
print(output.content)

# %% next run
messages.append(("ai", output.content))
messages.append(("user", "Der Hund jagt nach der Katze."))
prompt = ChatPromptTemplate.from_messages(messages)
chain = prompt | model
output = chain.invoke({})
print(output.content)

# %%

# %%
