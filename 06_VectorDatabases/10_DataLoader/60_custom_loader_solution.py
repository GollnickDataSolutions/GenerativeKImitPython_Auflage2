#%% Packages
from loaders import WebLoader
# %% The book details
book_details = {
    "title": "The Adventures of Sherlock Holmes",
    "author": "Arthur Conan Doyle",
    "year": 1892,
    "language": "English",
    "genre": "Detective Fiction",
    "url": "https://www.gutenberg.org/cache/epub/1661/pg1661.txt"
}

loader = WebLoader(url=book_details.get("url"), encoding="utf-8")
data = loader.load()

#%% Add metadata from book_details
data[0].metadata = book_details

# %%
data[0].metadata
# %%
