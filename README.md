# Generative KI mit Python – Codebeispiele zur 2. Auflage

Dieses Repository enthält alle Codebeispiele zum Buch **„Generative KI mit Python"** (2. Auflage,
Rheinwerk Verlag). Die Ordner sind nach Kapiteln benannt, die Dateien innerhalb eines Kapitels sind
durchnummeriert und folgen der Reihenfolge im Buch.

Diese Anleitung beschreibt, wie Sie die Arbeitsumgebung einrichten, die API-Schlüssel hinterlegen und
die Beispiele ausführen.

---

## 1. Voraussetzungen

| Was | Version / Hinweis |
| --- | --- |
| **Python** | 3.13 (das Projekt ist auf `>=3.13,<3.14` festgelegt) |
| **Git** | zum Klonen des Repositorys |
| **Editor** | empfohlen: VS Code mit den Erweiterungen *Python* und *Jupyter* |
| **Ollama** | nur für `04_LLMs/70_chat_ollama.py` (lokales Sprachmodell), [ollama.com](https://ollama.com) |

Die Beispiele in Kapitel 3 und 8 laden Modelle von Hugging Face herunter. Rechnen Sie beim ersten
Ausführen mit einigen Gigabyte Download und entsprechend Platz auf der Festplatte.

---

## 2. Repository klonen

```bash
git clone https://github.com/GollnickDataSolutions/GenerativeKImitPython_Auflage2.git
cd GenerativeKImitPython_Auflage2
```

---

## 3. Umgebung einrichten

Sie haben zwei Möglichkeiten. **Weg A mit `uv` ist der empfohlene Weg**, weil die exakten
Paketversionen in `uv.lock` festgehalten sind und Sie damit dieselbe Umgebung erhalten, die den
Beispielen im Buch zugrunde liegt. Weg B mit `venv` und `pip` ist der klassische Weg und funktioniert
ebenfalls.

### Weg A: `uv` (empfohlen)

[`uv`](https://docs.astral.sh/uv/) ist ein moderner Paket- und Umgebungsmanager für Python. Er
übernimmt drei Aufgaben in einem Schritt: die passende Python-Version besorgen, eine virtuelle
Umgebung anlegen und alle Pakete installieren.

**1. `uv` installieren** (nur einmal pro Rechner nötig):

```bash
pip install uv
```

Wer noch kein Python auf dem Rechner hat, findet in der
[Installationsanleitung von uv](https://docs.astral.sh/uv/getting-started/installation/) einen Weg
ohne Vorinstallation.

**2. Umgebung und Pakete installieren:**

```bash
uv sync
```

`uv sync` liest `pyproject.toml` und `uv.lock`, legt die virtuelle Umgebung `.venv` im
Projektverzeichnis an und installiert alle benötigten Pakete in den dort festgehaltenen Versionen.
Ein separates Aktivieren ist nicht nötig – Skripte starten Sie mit:

```bash
uv run 04_LLMs/10_model_chat_openai.py
```

### Weg B: `venv` und `pip`

**1. Virtuelle Umgebung anlegen und aktivieren**

Unter macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Unter Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Unter Windows (Eingabeaufforderung):

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

Ist die Umgebung aktiv, steht ihr Name in Klammern am Anfang der Eingabezeile: `(.venv)`.

**2. Pakete installieren**

Die benötigten Pakete sind in der Datei `requirements.txt` aufgelistet – nach Kapiteln gruppiert und
kurz kommentiert, sodass Sie nachvollziehen können, wofür jedes Paket gebraucht wird. Installieren
lassen sie sich mit:

```bash
pip install -r requirements.txt
```

Sollte ein einzelnes Paket Probleme machen, können Sie es auch gezielt nachinstallieren:

```bash
pip install <paketname>
```

> **Hinweis:** Anders als bei `uv sync` werden hier nicht die festgeschriebenen Versionen aus
> `uv.lock` verwendet, sondern jeweils die neuesten passenden. Bei neuen Paketversionen kann es
> deshalb zu Abweichungen gegenüber dem Buch kommen.

---

## 4. API-Schlüssel hinterlegen

Viele Beispiele greifen auf Dienste zu, die einen API-Schlüssel benötigen. Die Schlüssel werden
**nicht** in den Code geschrieben, sondern in eine Datei namens `.env` im Projekt-Wurzelverzeichnis.
Diese Datei ist in `.gitignore` eingetragen und landet damit nicht versehentlich auf GitHub.

Legen Sie die Datei `.env` neu an und tragen Sie die Schlüssel ein, die Sie benötigen:

```ini
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-...
TAVILY_API_KEY=tvly-...
PINECONE_API_KEY=pcsk_...
AGENTOPS_API_KEY=...
```

Welchen Schlüssel Sie für welches Kapitel brauchen:

| Schlüssel | Wird gebraucht in | Registrierung |
| --- | --- | --- |
| `OPENAI_API_KEY` | Kapitel 4 bis 9 und 11 – die meisten Beispiele | [platform.openai.com](https://platform.openai.com/api-keys) |
| `OPENROUTER_API_KEY` | Kapitel 4 und 8 – Zugriff auf Modelle anderer Anbieter | [openrouter.ai](https://openrouter.ai/keys) |
| `PINECONE_API_KEY` | Kapitel 6 und 7 – Vektordatenbank in der Cloud | [pinecone.io](https://www.pinecone.io/) |
| `TAVILY_API_KEY` | Kapitel 8 – Websuche als Werkzeug für Agenten | [tavily.com](https://tavily.com/) |
| `AGENTOPS_API_KEY` | Kapitel 8 – Beobachtung von Agenten | [agentops.ai](https://www.agentops.ai/) |

Sie brauchen nicht alle Schlüssel auf einmal. Für den Einstieg genügt `OPENAI_API_KEY`; die übrigen
können Sie ergänzen, sobald Sie beim entsprechenden Kapitel angekommen sind.

> **Kosten:** Die Dienste rechnen nach Nutzung ab. Die Beispiele im Buch sind bewusst klein gehalten,
> die Kosten bewegen sich im Bereich von Cent-Beträgen. Legen Sie im Konto des Anbieters dennoch ein
> Ausgabenlimit fest.

---

## 5. Einrichtung prüfen

Zwei Skripte im Wurzelverzeichnis prüfen, ob alles sitzt.

**Python-Version und Pakete prüfen:**

```bash
uv run test_python_env.py
```

Bei Weg B mit aktivierter Umgebung:

```bash
python test_python_env.py
```

Das Skript meldet die gefundene Python-Version, den verwendeten Interpreter und für jedes wichtige
Paket, ob es installiert ist.

**`.env`-Datei und OpenAI-Verbindung prüfen:**

```bash
uv run test_env.py
```

Das Skript sucht die `.env`-Datei, prüft die enthaltenen Schlüssel und baut eine Testverbindung zu
OpenAI auf.

---

## 6. Beispiele ausführen

**Starten Sie die Skripte immer aus dem Projekt-Wurzelverzeichnis.** Die Beispiele laden die
Schlüssel mit `load_dotenv(find_dotenv(usecwd=True))`, also relativ zum aktuellen
Arbeitsverzeichnis. Wechseln Sie stattdessen in einen Kapitelordner, wird die `.env`-Datei nicht
gefunden und die API-Aufrufe schlagen fehl.

```bash
# richtig
uv run 07_RAG/10_simple_RAG.py

# falsch
cd 07_RAG
uv run 10_simple_RAG.py
```

Die Dateien enthalten `#%%`-Markierungen. In VS Code werden daraus ausführbare Zellen: Sie können
einzelne Abschnitte mit **Shift + Enter** ausführen und die Zwischenergebnisse ansehen, ähnlich wie
in einem Notebook. Wählen Sie dazu über *Python: Select Interpreter* den Interpreter aus `.venv` aus.

Einige Beispiele greifen über Ordnergrenzen hinweg auf Code aus früheren Kapiteln zu – etwa
`07_RAG/10_simple_RAG.py` auf den Loader aus `06_VectorDatabases/10_DataLoader`. Verschieben oder
umbenennen sollten Sie die Ordner deshalb nicht.

---

## 7. Kapitel mit eigener Umgebung

Einige Beispiele benötigen Pakete, die sich mit denen der Hauptumgebung nicht vertragen. Für sie gibt
es jeweils eine eigene Umgebung. Das liegt an widersprüchlichen Versionsanforderungen der
Bibliotheken; die Kommentare in den jeweiligen Projektdateien nennen den Grund im Einzelnen.

### RAG-Evaluierung (`07_RAG/60_rag_eval.py`)

`ragas` benötigt eine ältere Version von `langchain-community`, als der `SemanticChunker` aus
Kapitel 6 sie verlangt. Deshalb eine zweite Umgebung:

```bash
uv venv --python 3.13 .venv-ragas
uv pip install --python .venv-ragas -r 07_RAG/requirements_ragas.txt
uv run --python .venv-ragas 07_RAG/60_rag_eval.py
```

### Agenten-Frameworks in Kapitel 8

Die Unterordner `pydantic_ai`, `openai_agents`, `ai_security` und `crewAI/news_analysis` sind
eigenständige Projekte mit eigener `pyproject.toml`. Wechseln Sie in den Ordner und richten Sie die
Umgebung dort ein:

```bash
cd 08_AgenticSystems/pydantic_ai
uv sync
uv run pydantic_ai_intro.py
```

### Deployment in Kapitel 11

`11_Deployment/streamlit` und `11_Deployment/heroku` haben jeweils eine eigene `requirements.txt`,
weil sie für den Betrieb auf einem Server gedacht sind. Die `README`-Dateien in diesen Ordnern
beschreiben die Veröffentlichung.

---

## 8. Verzeichnisstruktur

| Ordner | Inhalt |
| --- | --- |
| `03_PreTrainedNetworks` | Vortrainierte Modelle: Zusammenfassung, Übersetzung, Bild- und Audioerzeugung, NER, Question Answering |
| `04_LLMs` | Große Sprachmodelle: Chat-Modelle, Prompt-Vorlagen, Chains, Multimodalität, Ollama |
| `05_PromptEngineering` | Few-Shot, Prompt Chaining, Self-Consistency, Self-Feedback |
| `06_VectorDatabases` | Laden, Chunking, Embeddings, Vektorspeicher (Chroma, Pinecone), Retrieval |
| `07_RAG` | Retrieval Augmented Generation: einfaches RAG, Hybrid-Suche, Caching, Evaluierung |
| `08_AgenticSystems` | Agentensysteme mit LangGraph, CrewAI, Pydantic AI, OpenAI Agents SDK, MS Agent Framework |
| `09_MCP` | Model Context Protocol: eigener MCP-Server |
| `10_AgenticCoding` | Agentic Coding: Beispieldaten für die Übungen des Kapitels |
| `11_Deployment` | Veröffentlichung: Streamlit-App, REST-API mit FastAPI, Heroku |

---

## 9. Häufige Probleme

**`ModuleNotFoundError`, obwohl das Paket installiert ist**
Es läuft der falsche Interpreter. Prüfen Sie mit `uv run test_python_env.py`, welcher Interpreter
verwendet wird. In VS Code wählen Sie über *Python: Select Interpreter* die Umgebung `.venv` aus.

**`AuthenticationError` oder fehlender API-Schlüssel**
Die `.env`-Datei wurde nicht gefunden, oder der Schlüssel fehlt. Starten Sie das Skript aus dem
Projekt-Wurzelverzeichnis und prüfen Sie die Einrichtung mit `uv run test_env.py`.

**Fehler beim Installieren von `torch`**
`torch` ist ein großes Paket und braucht eine passende Python-Version. Stellen Sie sicher, dass Sie
Python 3.13 verwenden (`python --version`).

**Ein Beispiel bricht mit einem Versionskonflikt ab**
Prüfen Sie, ob es zu den Fällen in Abschnitt 7 gehört und eine eigene Umgebung benötigt.

**Ein Beispiel liefert eine andere Antwort als im Buch**
Sprachmodelle antworten nicht deterministisch. Abweichungen im Wortlaut sind normal; entscheidend
ist, dass der Ablauf funktioniert.

---

## Rückmeldungen

Fehler oder Verbesserungsvorschläge gerne als
[Issue](https://github.com/GollnickDataSolutions/GenerativeKImitPython_Auflage2/issues) in diesem
Repository melden.
