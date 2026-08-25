#%% packages
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
load_dotenv()
# %% Model and Embeddings Setup
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings()

#%% Prompt Templates
template_math = "Löse die folgende Matheaufgabe: {user_input}, sag, dass du ein Mathe-Agent bist"
template_music = "Vorschlage ein Lied für den Benutzer: {user_input}, sag, dass du ein Musik-Agent bist"
template_history = "Biete eine Geschichte für den Benutzer: {user_input}, sag, dass du ein Geschichte-Agent bist"


# %% Math-Chain
prompt_math = ChatPromptTemplate.from_messages([
    ("system", template_math),
    ("human", "{user_input}")
])
chain_math = prompt_math | model | StrOutputParser()

# %% Music-Chain
prompt_music = ChatPromptTemplate.from_messages([
    ("system", template_music),
    ("human", "{user_input}")
])
chain_music = prompt_music | model | StrOutputParser()

#%% 
# History-Chain
prompt_history = ChatPromptTemplate.from_messages([
    ("system", template_history),
    ("human", "{user_input}")
])
chain_history = prompt_history | model | StrOutputParser()

#%% combine all chains
chains = [chain_math, chain_music, chain_history]

# %% Create Prompt Embeddings
chain_embeddings = embeddings.embed_documents(["math", "music", "history"])
#%%
print(len(chain_embeddings))

# %% Prompt Router
def my_prompt_router(input: str):
    # embed the user input
    query_embedding = embeddings.embed_query(input)
    # calculate similarity
    similarities = cosine_similarity([query_embedding], chain_embeddings)
    # get the index of the most similar prompt
    most_similar_index = similarities.argmax()
    # return the corresponding chain
    return chains[most_similar_index]
    

#%% Testing the Router
# query = "Was ist die Quadratwurzel von 16?"
# query = "Was passiert während der französischen Revolution?"
query = "Wer komponierte das Mondscheinsonate?"
chain = my_prompt_router(query)
print(chain.invoke(query))

# %%