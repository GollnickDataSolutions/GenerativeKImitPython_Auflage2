#%% packages
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from langchain_arxiv.retriever import ArxivRetriever

#%% model selection
# Hinweis: Transformers 5 kennt keine "summarization"-Pipeline mehr,
# das Seq2Seq-Modell wird daher direkt geladen.
model_name = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

#%% Data Preparation
query = "artificial general intelligence"
retriever = ArxivRetriever(k=1, full_text=True)
docs = retriever.invoke(query)

# %% Data Preparation
article_text = docs[0].page_content

# %% Tokenisierung
# Das Modell verarbeitet maximal 1024 Tokens, längere Texte werden abgeschnitten.
inputs = tokenizer(article_text, max_length=1024, truncation=True, return_tensors="pt")

# %% Zusammenfassung erzeugen
summary_ids = model.generate(
    **inputs,
    min_length=20,
    max_length=80,
    num_beams=4,
    length_penalty=2.0,
    no_repeat_ngram_size=3,
    do_sample=False,
)
summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#%%
print(summary_text)

# %% number of words
print(len(summary_text.split(' ')))

# %%
