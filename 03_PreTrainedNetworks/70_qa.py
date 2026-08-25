#%% packages
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

#%% model selection
# Hinweis: Transformers 5 kennt keine "question-answering"-Pipeline mehr
# ("document-question-answering" erwartet ein Bild), das Modell wird
# daher direkt geladen.
MODEL = "deepset/roberta-base-squad2"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForQuestionAnswering.from_pretrained(MODEL)

#%% Data Preparation
question = 'What are the benefits of remote work?'
context = 'Remote work allows employees to work from anywhere, providing flexibility and a better work-life balance. It reduces commuting time, lowers operational costs for companies, and can increase productivity for self-motivated workers.'

# %% Antwort extrahieren
# Das Modell sagt vorher, an welcher Position die Antwort
# beginnt (start_logits) und endet (end_logits).
inputs = tokenizer(question, context, return_tensors="pt")
outputs = model(**inputs)
start = int(outputs.start_logits.argmax())
end = int(outputs.end_logits.argmax())
answer = tokenizer.decode(inputs['input_ids'][0][start:end + 1],
                          skip_special_tokens=True).strip()

#%%
print(answer)

# %%
