#%% packages
import os
import sys
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "06_VectorDatabases","10_DataLoader"
    )
)
from loaders import WikipediaLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
from langchain_openrouter import ChatOpenRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
#%% load dataset
persist_directory = "rag_store"
if os.path.exists(persist_directory):
    vector_store = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())
else:
    data = WikipediaLoader(
        query="Human History",
        load_max_docs=5,
        doc_content_chars_max=10000,
    ).load()

    # split the data
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(data)

    # create persistent vector store
    vector_store = Chroma.from_documents(chunks, embedding=OpenAIEmbeddings(), persist_directory="rag_store")

#%% 
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
question = "Was ist in der Geschichte der menschlichen Zivilisation passiert?"
relevant_docs = retriever.invoke(question)

#%% print content of relevant docs
for doc in relevant_docs:
    print(doc.page_content[: 100])
    print("\n--------------")

#%% combined relevant docs to context
context = "\n".join([doc.page_content for doc in relevant_docs])

#%% create prompt
messages = [
    ("system", "Du bist ein KI-Assistent, der Fragen zur Geschichte der menschlichen Zivilisation beantworten kann. Du erhältst eine Frage und eine Liste von Dokumenten und sollst die Frage ausschließlich auf Basis dieser Dokumente beantworten. Diese Dokumente können dir helfen, die Frage zu beantworten: <context>{context}</context>. Wenn du dir bei der Antwort nicht sicher bist, kannst du sagen: 'Ich weiß es nicht' oder 'Ich kenne die Antwort auf diese Frage nicht.'"),
    ("human", "<question>{question}</question>"),
]
prompt = ChatPromptTemplate.from_messages(messages=messages)


#%% create model and chain
parser = StrOutputParser()
MODEL_NAME = "moonshotai/kimi-k3"
model = ChatOpenRouter(model=MODEL_NAME)
chain = prompt | model | parser

#%% invoke chain
answer = chain.invoke({"question": question, "context": context})
print(answer)



# %% bundle everything in a function
def simple_rag_system(question: str) -> str:
    relevant_docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    messages = [
    ("system", "Du bist ein KI-Assistent, der Fragen zur Geschichte der menschlichen Zivilisation beantworten kann. Du erhältst eine Frage und eine Liste von Dokumenten und sollst die Frage ausschließlich auf Basis dieser Dokumente beantworten. Diese Dokumente können dir helfen, die Frage zu beantworten: <context>{context}</context>. Wenn du dir bei der Antwort nicht sicher bist, kannst du sagen: 'Ich weiß es nicht' oder 'Ich kenne die Antwort auf diese Frage nicht.'"),
    ("human", "<question>{question}</question>"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages=messages)
    chain = prompt | model | parser
    answer = chain.invoke({"question": question, "context": context})
    return answer

#%% Testing the function
question = "Was ist ein schwarzes Loch?"
simple_rag_system(question=question)