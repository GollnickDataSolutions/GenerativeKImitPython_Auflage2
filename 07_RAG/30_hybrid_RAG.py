#%% packages
from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings 
import os
load_dotenv()
# %%
os.getenv("PINECONE_API_KEY")
# %%
# %% connect to Pinecone instance
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "sherlock"
index = pc.Index(name=index_name)
# %%
print(index.describe_index_stats())
#%%
#%% Embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

#%% embed user query
user_query = "How does the hound look like?"
query_embedding = embedding_model.embed_query(user_query)

#%% search for similar documents
res = index.query(vector=query_embedding, top_k=2, include_metadata=True)

# %%
res
# %%
