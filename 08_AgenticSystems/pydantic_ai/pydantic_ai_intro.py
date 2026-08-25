#%%
import wikipedia
from langchain_classic.document_loaders import WikipediaLoader
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

#%% user agent setzen
# der WikipediaLoader nutzt intern das Paket wikipedia, dessen Standard-
# User-Agent von Wikimedia abgelehnt wird. Die Policy verlangt eine
# Kontaktangabe (URL oder E-Mail) - ohne sie antwortet die API mit 429.
# Das Paket prueft den Status nicht, deshalb kommt der Fehler als
# JSONDecodeError an.

wikipedia.set_user_agent(
    "GenerativeKI-Buch/2.0 "
    "(https://github.com/GollnickDataSolutions/Buch_GenerativeKImitPython_Auflage2)"
)
# wartet zwischen den API-Aufrufen und haelt so die Rate-Limits ein
wikipedia.set_rate_limiting(True)

#%% load wikipedia article on Alan Turing
loader = WikipediaLoader(query="Alan Turing", load_all_available_meta=True, doc_content_chars_max=100000, load_max_docs=1)
doc = loader.load()

#%% extract page content
page_content = doc[0].page_content

#%% define pydantic model
class PersonDetails(BaseModel):
    date_born: str = Field(description="Das Geburtsdatum der Person im Format JJJJ-MM-TT")
    date_died: str = Field(description="Das Sterbedatum der Person im Format JJJJ-MM-TT")
    publications: list[str] = Field(description="Eine Liste von Veröffentlichungen der Person")
    achievements: list[str] = Field(description="Eine Liste von Errungenschaften der Person")
    
# %% agent instance
# seit pydantic-ai 2.0 heisst der Parameter output_type (frueher result_type);
# der Modellname braucht zwingend ein Provider-Praefix wie "openai:"
MODEL = "openai:gpt-5.6-luna"
agent = Agent(model=MODEL, output_type=PersonDetails)
result = agent.run_sync(page_content)

# %% print result
# das Ergebnis steht in result.output (frueher result.data)
print(result.output.model_dump())
