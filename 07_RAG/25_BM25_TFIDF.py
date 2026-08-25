#%% packages
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from typing import List
import string
#%% Documents
def preprocess_text(text: str) -> List[str]:
    # Remove punctuation and convert to lowercase
    text = text.lower()
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()

corpus = [
    "Künstliche Intelligenz ist ein Bereich der künstlichen Intelligenz. Das Gebiet der künstlichen Intelligenz beinhaltet maschinelles Lernen. Maschinelles Lernen ist ein Feld der künstlichen Intelligenz. Künstliche Intelligenz entwickelt sich rasant weiter.",
    "Roboter mit künstlicher Intelligenz übernehmen die Welt. Roboter sind Maschinen, die alles tun können, was ein Mensch tun kann. Roboter übernehmen die Welt. Roboter übernehmen die Welt.",
    "Das Wetter in tropischen Regionen ist typischerweise warm. Warmes Wetter ist in diesen Regionen üblich und beeinflusst sowohl das tägliche Leben als auch die natürlichen Ökosysteme. Das warme und feuchte Klima ist ein prägendes Merkmal dieser Regionen.",
    "Das Klima in verschiedenen Teilen der Welt unterscheidet sich. Wetterphänomene ändern sich aufgrund geografischer Gegebenheiten. Einige Regionen erleben Regen, während andere trocken sind."
]

# Preprocess the corpus
tokenized_corpus = [preprocess_text(doc) for doc in corpus]
# %% Sparse Search (BM25)
bm25 = BM25Okapi(tokenized_corpus)

#%% Set up user query
user_query = "warmes Wetter in tropischen Regionen"

tokenized_query_BM25 = user_query.lower().split()
tokenized_query_tfidf = ' '.join(tokenized_query_BM25)
# Process query to remove stop words

bm25_similarities = bm25.get_scores(tokenized_query_BM25)
print(f"Tokenized Query BM25: {tokenized_query_BM25}")
print(f"Tokenized Query TFIDF: {tokenized_query_tfidf}")
print(f"BM25 Similarities: {bm25_similarities}")

#%% calculate tfidf
tfidf = TfidfVectorizer()
tokenized_corpus_tfidf = [' '.join(words) for words in tokenized_corpus]
tfidf_matrix = tfidf.fit_transform(tokenized_corpus_tfidf)

query_tfidf_vec = tfidf.transform([tokenized_query_tfidf])
tfidf_similarities = cosine_similarity(query_tfidf_vec, tfidf_matrix).flatten()
print(f"TFIDF Similarities: {tfidf_similarities}")

# %%
