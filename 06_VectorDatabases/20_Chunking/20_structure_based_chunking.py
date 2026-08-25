#%% Packages
import os
import sys

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "10_DataLoader"
    )
)
from loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#%% Path Handling
# Get the current working directory
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

# Go up one directory level
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, "data", "HoundOfBaskerville.txt")

#%% load all files in a directory
loader = TextLoader(file_path=file_path, 
                    encoding="utf-8")
docs = loader.load()

# %%
docs

# %% Set up the splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=4000, 
                                         chunk_overlap=400,
                                          separators=["\n\n", "\n"," ", ".", ","])

# %% Create the chunks
doc_chunks = splitter.split_documents(docs)
# %% Number of chunks
len(doc_chunks)


# %%
# %% visualize the chunk size (6)
import seaborn as sns
import matplotlib.pyplot as plt
# get number of characters in each chunk
chunk_lengths = [len(chunk.page_content) for chunk in doc_chunks]

sns.histplot(chunk_lengths, bins=50, binrange=(0, 4100))
# add title
plt.title("Verteilung der Chunk-Längen")
# add x-axis label
plt.xlabel("Anzahl der Zeichen")
# add y-axis label
plt.ylabel("Anzahl der Chunks")

# %%
