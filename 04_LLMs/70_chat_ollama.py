#%% packages
from langchain_ollama import ChatOllama

#%% ollama
model = ChatOllama(model="qwen3.5:2b")
response = model.invoke("Was ist ein LLM?")

# %%
print(response.content)

