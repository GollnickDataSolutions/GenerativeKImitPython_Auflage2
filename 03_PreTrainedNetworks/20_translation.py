#%% packages
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

#%% model selection
# Hinweis: Transformers 5 kennt keine "translation"-Pipeline mehr,
# das Seq2Seq-Modell wird daher direkt geladen.
model_name = "Mitsua/elan-mt-bt-en-ja"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# %% Tokenisierung
text = "Be the change you wish to see in the world."
inputs = tokenizer(text, return_tensors="pt")

# %% Übersetzung erzeugen
translated_ids = model.generate(**inputs, max_length=128, num_beams=4)
translation_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

#%%
print(translation_text)

# %%
