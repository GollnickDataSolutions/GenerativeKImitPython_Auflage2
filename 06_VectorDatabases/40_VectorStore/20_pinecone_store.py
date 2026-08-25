#%% packages
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
load_dotenv()
# %%
os.getenv("PINECONE_API_KEY")
# %% connect to Pinecone instance
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# %% 
index_name = "sherlock2"
if index_name not in pc.list_indexes().names():
    pc.create_index(name=index_name, 
                    metric="cosine", 
                    dimension=1536,
                    spec=ServerlessSpec(
                        cloud = "aws",
                        region="us-east-1"))
# %% Prepare data
from data_prep import create_chunks
chunks = create_chunks("HoundOfBaskerville.txt")
# limit to the first 10 chunks
chunks = chunks[:10]

texts = [chunk.page_content for chunk in chunks]


# %% Embedding model
from langchain_openai import OpenAIEmbeddings 
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
# %% create all embeddings
embeddings = embedding_model.embed_documents(texts=texts)

# %% create vectors
# {"id": str, "values": List[float], "metadata": Dict[str, str]}
# der Chunk-Text muss mit in die Metadaten, sonst geht er beim Retrieval verloren
vectors = [{"id": str(i),
            "values": embeddings[i],
            "metadata": {**chunks[i].metadata, "text": texts[i]}}
           for i in range(len(chunks))]
# %%
index = pc.Index(name=index_name)
index.upsert(vectors)

#%% describe index
print(index.describe_index_stats())

# %%
