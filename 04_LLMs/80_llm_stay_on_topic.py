#%% packages
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter

from langchain_core.output_parsers import StrOutputParser
from transformers import pipeline
from dotenv import load_dotenv, find_dotenv

load_dotenv()
#%%
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
# %%
def guard_medical_prompt(prompt: str) -> str:
    candidate_labels = ["politics", "finance", "technology", "healthcare", "sports"]
    result = classifier(prompt, candidate_labels)
    if result["labels"][0] == "healthcare":
        return "valid"
    else:
        return "invalid"

#%% TEST guard_medical_prompt
user_prompt = "Should I buy stocks of Apple, Google, or Amazon?"
user_prompt = "I have headache"
guard_medical_prompt(user_prompt)

# %% guarded chain
def guarded_chain(user_input: str):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Du bist ein hilfreicher Assistent, der Fragen zu Gesundheit beantworten kann."),
        ("user", "{input}"),
    ])

    model = ChatOpenRouter(model="google/gemini-3.1-flash-lite")

    # Guard step
    if guard_medical_prompt(user_input) == "invalid":
        return "Entschuldigung, ich kann nur Fragen zu Gesundheit beantworten."
    
    # Proceed with the chain
    chain = prompt_template | model | StrOutputParser()
    return chain.invoke({"input": user_input})

# %% TEST guarded_chain
user_prompt = "Should I buy stocks of Apple, Google, or Amazon?"
# user_prompt = "I have a headache"
guarded_chain(user_prompt)
# %%
