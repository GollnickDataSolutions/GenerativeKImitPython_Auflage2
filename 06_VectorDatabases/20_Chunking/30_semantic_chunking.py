#%% Packages (1)
import os
import sys
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "10_DataLoader"
    )
)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from pprint import pprint
from loaders import TextLoader
from dotenv import load_dotenv
load_dotenv()
# %% Load the book 
loader = TextLoader("../data/HoundOfBaskerville.txt")
doc = loader.load()

#%% limit doc[0].page_content to 1000 characters
doc[0].page_content = doc[0].page_content[:1000]

# %% check the content (3)
pprint(doc[0].page_content)
# %% Create splitter instance (4)
splitter = SemanticChunker(embeddings=OpenAIEmbeddings(), 
                           breakpoint_threshold_type="percentile", 
                           breakpoint_threshold_amount=0.5)

# %% Apply semantic chunking (5)
chunks = splitter.split_documents(doc)

# %% check the results (6)
chunks
# %%
pprint(chunks[0].page_content)
# %%
pprint(chunks[1].page_content)
# %%
