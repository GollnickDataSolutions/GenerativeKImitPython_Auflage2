#%% packages
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
load_dotenv()

#%% function for Chain-of-Thought Prompting
def chain_of_thought_prompting(prompt: str, model_name: str = "google/gemma-2-27b-it") -> str:
    model = ChatOpenRouter(model_name=model_name)
    prompt = ChatPromptTemplate.from_messages(messages=[
        ("system", "Du bist ein hilfreicher Assistent und antwortest präzise und knapp. Antworte auf Deutsch."),
   
        ("user", f"{prompt} \n think step by step")
    ])
    # print(prompt)
    chain = prompt | model
    return chain.invoke({}).content


# %% Self-Consistency CoT
def self_consistency_cot(prompt: str, number_of_runs: int = 3) -> str:
    # run CoT multiple times
    res = []
    for _ in range(number_of_runs):
        current_res = chain_of_thought_prompting(prompt)
        print(current_res)
        res.append(current_res)
    
    # concatenate all results
    res_concat = ";".join(res)
    self_consistency_prompt = f"Du erhältst mehrere Antworten in <<>>, getrennt durch ; <<{res_concat}>>. Extrahiere nur die finalen Gleichungen und gib die am häufigsten vorkommende Gleichung exakt so zurück, wie sie ursprünglich angegeben wurde. Falls es keine gemeinsame Gleichung gibt, gib die wahrscheinlichste Gleichung zurück. Antworte auf Deutsch."
    self_consistency_prompt_concat = ";".join(self_consistency_prompt)
    messages = [
        ("system", "Du bist ein hilfreicher Assistent und antwortest präzise und knapp."),
        ("user", f"{self_consistency_prompt_concat}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages=messages)
    model = ChatOpenRouter(model_name="google/gemini-3.6-flash")
    chain = prompt | model
    return chain.invoke({}).content


#%% Test
user_prompt = "Das Ziel des Spiels 24 ist es, mit den vier Grundrechenarten (Addition, Subtraktion, Multiplikation und Division) vier Zahlen so zu kombinieren, dass das Ergebnis 24 ist. Die Zahlen sind 3, 4, 6 und 8. Es ist verpflichtend, alle vier Zahlen zu verwenden. Bitte überprüfe die endgültige Gleichung auf Korrektheit. Hinweise: Identifiziere die Grundoperationen, priorisiere Multiplikation und Division, suche nach Kombinationen, die durch 24 teilbar sind, beachte die Reihenfolge der Rechenoperationen, setze Klammern strategisch ein und übe mit verschiedenen Zahlenkombinationen."

# %%
res = chain_of_thought_prompting(prompt=user_prompt)
#%%
res = self_consistency_cot(prompt=user_prompt, number_of_runs=5)
pprint(res)
# %%
from pyperclip import copy 
copy(res)

# %%
