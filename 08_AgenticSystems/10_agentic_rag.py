#%% packages
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_classic.vectorstores import FAISS
from langchain_classic.document_loaders import WikipediaLoader
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()


# Load documents for retrieval (can be replaced with any source of text)
# Here we're using a text loader with some sample text files as an example
#%% import wikipedia
loader = WikipediaLoader("Principle of relativity",     
                         load_max_docs=10)
docs = loader.load()

#%% create chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)


#%% models and tools
llm = ChatOpenAI(model="gpt-5.6-luna")
embedding = OpenAIEmbeddings()
search_tool = TavilySearch(max_results=5, include_answer=True)

#%% use FAISS to store the chunks
vectorstore = FAISS.from_documents(chunks, embedding)
retriever = vectorstore.as_retriever(return_similarities=True)

#%% user query

query = "Wie ist die Relativitätstheorie definiert?"
#%% RAG chain
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
     Du bist ein hilfreicher Assistent, der Fragen zum Relativitätsprinzip beantworten kann. Du erhältst Kontextinformationen aus den abgerufenen Dokumenten. Wenn du die Antwort nicht kennst, sage einfach "unzureichende Informationen".

     """),
    ("user", "<context>{context}</context>\n\n<question>{question}</question>"),
])
retrieved_docs = retriever.invoke(query)
retrieved_docs_str = ";".join([doc.page_content for doc in retrieved_docs])
chain = prompt_template | llm
rag_response = chain.invoke({"question": query, 
                             "context": retrieved_docs_str})
#%%

if rag_response.content == "unzureichende Informationen":
    print("Verwende Suchtool")
    final_response = search_tool.invoke({"query": query})
    final_response_str = ";".join([doc['content'] for doc in final_response])
    final_response = chain.invoke({"question": query, 
                                     "context": final_response_str})
else:
    print("Vektorspeicher wird verwendet")
    final_response = rag_response.content

final_response

# %%
from pyperclip import copy
copy(final_response)
# %%