#%% (1) Packages
import os
from loaders import TextLoader

#%% (3) File Handling
# Get the current working directory
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

# Go up one directory level
parent_dir = os.path.dirname(current_dir)

file_path = os.path.join(parent_dir, "data","HoundOfBaskerville.txt")
file_path

#%% (4) Load a single document
text_loader = TextLoader(file_path=file_path, encoding="utf-8")
doc = text_loader.load()

#%% (5) Understand the document
# Metadata
doc[0].metadata

# %% Page content
doc[0].page_content

# %%
