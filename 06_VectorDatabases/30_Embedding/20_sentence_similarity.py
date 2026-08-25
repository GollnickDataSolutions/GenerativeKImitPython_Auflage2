#%% (1) Packages
from sentence_transformers import SentenceTransformer
import numpy as np
import seaborn as sns
#%% (2) Load the model
MODEL = 'sentence-transformers/distiluse-base-multilingual-cased-v1'
model = SentenceTransformer(MODEL)
# %% (3) Define the sentences
sentences = [
    'The cat lounged lazily on the warm windowsill.',
    'A feline relaxed comfortably on the sun-soaked ledge.',
    'The kitty reclined peacefully on the heated window perch.',
    'Quantum mechanics challenges our understanding of reality.',
    'The chef expertly julienned the carrots for the salad.',
    'The vibrant flowers bloomed in the garden.',
    'Las flores vibrantes florecieron en el jardín. ',
    'Die lebhaften Blumen blühten im Garten.'
]
# %% (4) Get the embeddings
sentence_embeddings = model.encode(sentences)

# %% (5) Calculate linear correlation matrix for embeddings
sentence_embeddings_corr = np.corrcoef(sentence_embeddings)

# %% (6) Plot the correlation matrix as a heatmap
import textwrap  # Package for wrapping the long sentences into several lines
import matplotlib.pyplot as plt

# the full sentences label both axes, wrapped into short lines
labels = [f"{i}  {textwrap.fill(s.strip(), 28)}"
          for i, s in enumerate(sentences, start=1)]

fig, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(sentence_embeddings_corr, annot=True,
            fmt=".1f",
            square=True,
            cmap="rocket",
            xticklabels=labels,
            yticklabels=labels,
            cbar_kws={"shrink": 0.5, "label": "Korrelation"},
            ax=ax)
ax.tick_params(axis="y", rotation=0)  # keep the row labels horizontal
# turn the column labels upright: tilted ones would run into each other
plt.setp(ax.get_xticklabels(), rotation=90, ha="center", va="top",
         multialignment="right")

# %% (7) save image
fig.savefig("sentence_similarity.png", dpi=200, bbox_inches="tight")
