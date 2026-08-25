#%% packages
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv, find_dotenv
load_dotenv()

#%%
messages = [
    ("system", "Du bist ein Kundenservice-Spezialist, der für Empathie, Professionalität und Problemlösung bekannt ist. Deine Antworten sind herzlich und dennoch professionell, lösungsorientiert und enden immer mit einem konkreten nächsten Schritt oder einer Lösung. Du behandelst sowohl Routineanfragen als auch eskalierte Anliegen mit gleicher Sorgfalt."),
    ("user", """
     Beispiel 1:
     Kunde: Ich habe bei meiner Bestellung #12345 ein Hemd in der falschen Größe erhalten.
     Antwort: Es tut mir sehr leid wegen des Größenproblems mit Ihrer Hemdbestellung. Das ist sicherlich enttäuschend! Ich kann das sofort für Sie in Ordnung bringen. Sie haben zwei Möglichkeiten:

     Ich kann Ihnen ein Rücksendeetikett schicken und die richtige Größe umgehend versenden.
     Alternativ kann ich auch eine vollständige Rückerstattung veranlassen, wenn Sie das wünschen.

     Welche Option passt besser für Sie? Sobald Sie mir Bescheid geben, kümmere ich mich sofort darum.
     Beispiel 2:
     Kunde: Ihre Website lässt mich meine Zahlungsmethode nicht aktualisieren.
     Antwort: Ich verstehe, wie frustrierend technische Probleme sein können, besonders wenn es um wichtige Informationen wie die Zahlungsdaten geht. Lassen Sie mich Ihnen Schritt für Schritt helfen:
     Könnten Sie zunächst versuchen, Ihren Browser-Cache und die Cookies zu löschen?
     Falls das nicht hilft, kann ich die Aktualisierung auch direkt von meiner Seite aus vornehmen.
     Könnten Sie mir bitte Ihre E-Mail-Adresse mitteilen, damit ich Ihnen weiterhelfen kann?
     Neue Anfrage: {customer_request}
     """
     ),
]
prompt = ChatPromptTemplate.from_messages(messages)
MODEL_NAME = 'openai/gpt-5.6-luna'
model = ChatOpenRouter(model_name=MODEL_NAME)
chain = prompt | model
# %%
res = chain.invoke({"customer_request": "Ich habe meine Rückerstattung noch nicht erhalten, obwohl ich den Artikel vor 2 Wochen zurückgeschickt habe."})

# %%
res.model_dump()['content']
# %%
from pyperclip import copy
copy(res.model_dump()['content'])
# %%
