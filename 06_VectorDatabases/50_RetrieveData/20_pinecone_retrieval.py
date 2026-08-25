#%% packages
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings 
import os
load_dotenv()

#%% connect to Pinecone instance
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "sherlock2"
index = pc.Index(name=index_name)

#%% Embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

#%% embed user query
user_query = "How does the hound look like?"
query_embedding = embedding_model.embed_query(user_query)

#%% search for similar documents
res = index.query(vector=query_embedding, top_k=2, include_metadata=True)

#%% get the matches
res["matches"]

#%% get the text metadata for the matches
for match in res['matches']:
    print(f"Score: {match['score']:.3f}")
    print(match['metadata']['text'])
    print("---------------")

# %%
