#%% (1) Packages
import os
import sys

# loaders.py liegt im Nachbarordner 10_DataLoader. Damit der Import gelingt,
# muss dieser Ordner erst dem Modul-Suchpfad hinzugefügt werden.
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "10_DataLoader"
    )
)

from langchain_text_splitters import CharacterTextSplitter
from loaders import DirectoryLoader, TextLoader
#%% (2) Path Handling
# Get the current working directory
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

# Go up one directory level
parent_dir = os.path.dirname(current_dir)
text_files_path = os.path.join(parent_dir, "data")

#%% (3) load all files in a directory
dir_loader = DirectoryLoader(path=text_files_path, 
                             glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'} )
docs = dir_loader.load()

# %%
docs

# %% Splitting text
# Packages
from langchain_text_splitters import CharacterTextSplitter
# Split by characters (2)
splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=400, separator=" ")
# %%
docs_chunks = splitter.split_documents(docs)
# %% Check the number of chunks
len(docs_chunks)
# %% check some random Documents (5)
from pprint import pprint
pprint(docs_chunks[100].page_content)
# %%
pprint(docs_chunks[101].page_content)

# %% visualize the chunk size (6)
import seaborn as sns
import matplotlib.pyplot as plt
# get number of characters in each chunk
chunk_lengths = [len(chunk.page_content) for chunk in docs_chunks]

sns.histplot(chunk_lengths, bins=50, binrange=(3950, 4050))
# add title
plt.title("Verteilung der Chunk-Längen")
# add x-axis label
plt.xlabel("Anzahl der Zeichen")
# add y-axis label
plt.ylabel("Anzahl der Chunks")
# %%
