#%% packages
from langchain_chroma import Chroma
import os
from pprint import pprint
from langchain_openai import OpenAIEmbeddings
# %% set up database connection
# Get the current working directory
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)
parent_dir = os.path.dirname(current_dir)
chroma_dir = os.path.join(parent_dir, "db")
# Go up one directory level
parent_dir = os.path.dirname(current_dir)
# set up the embedding function
embedding_function = OpenAIEmbeddings(
    model="text-embedding-3-small")
# connect to the database
db = Chroma(persist_directory=chroma_dir, 
            embedding_function=embedding_function)
# %%
retriever = db.as_retriever()
# %% find information
# query = "Who is the sidekick of Sherlock Holmes in the book?"

# # thematic search
# query = "Find passages that describe the moor or its atmosphere."

# # Emotion
# query = "Which chapters or passages convey a sense of fear or suspense?"

# # Dialogue Analysis
# query = "Identify all conversations between Sherlock Holmes and Dr. Watson."

# Character
query = "How does the hound look like?"
most_similar_docs = retriever.invoke(query)
# %%
pprint(most_similar_docs[0].page_content)
# %%
