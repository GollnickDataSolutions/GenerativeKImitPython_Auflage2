#%% packages
# ACHTUNG: Dieses Skript laeuft NICHT im Haupt-Environment (.venv), sondern
# braucht .venv-ragas -- in VS Code oben rechts als Kernel auswaehlen.
# Grund und Einrichtung: siehe requirements_ragas.txt im gleichen Ordner.
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import AnswerRelevancy, ContextPrecision, Faithfulness
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
# %%
my_sample = {
    "user_input": ["What is the capital of Germany in 1960?"],  # The main question
    "retrieved_contexts": [
        [
            "Berlin is the capital of Germany.",
            "Between 1949 and 1990, East Berlin was the capital of East Germany.",
            "Bonn was the capital of West Germany during the same period."
        ]
    ],  # Nested list for multiple contexts
    "response": ["In 1960, the capital of Germany was Bonn. East Berlin was the capital of East Germany."],
    "reference": ["Berlin"]
}

dataset = Dataset.from_dict(my_sample)
# %%
# bypass_temperature=True ist noetig, weil ragas intern temperature=0.01 setzt,
# Reasoning-Modelle wie gpt-5.5 aber nur den Default 1 akzeptieren.
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-5.5"), bypass_temperature=True)
evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))
metrics = [
    ContextPrecision(llm=evaluator_llm),
    AnswerRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
    Faithfulness(llm=evaluator_llm),
]
res = evaluate(dataset=dataset, metrics=metrics)
print(res)

# %%
