# Pydantic AI

Beispiele zu [Pydantic AI](https://ai.pydantic.dev/) (Version 2.x).

## Eigene Umgebung

Diese Beispiele laufen **nicht** in der Umgebung des Hauptprojekts: `pydantic-ai` importiert
`opentelemetry._events`, das in `opentelemetry-api` 1.44 entfernt wurde — das Hauptprojekt zieht
über `agent-framework` und `mcp` aber genau `opentelemetry-api>=1.44`. Deshalb hat dieser Ordner
ein eigenes `pyproject.toml`:

```bash
cd Code/08_AgenticSystems/pydantic_ai
uv sync
```

In VS Code anschließend `Code/08_AgenticSystems/pydantic_ai/.venv` als Interpreter auswählen.

Der `OPENAI_API_KEY` wird aus der `.env` im Projekt-Hauptverzeichnis geladen.

Für `pydantic_ai_logfire.py` ist zusätzlich ein Logfire-Zugang nötig — sonst bricht
`logfire.configure()` mit einem `LogfireConfigError` ab:

```bash
uv run logfire auth
```

Alternativ ein Write-Token als `LOGFIRE_TOKEN` setzen.

## Skripte

| Skript | Inhalt |
| --- | --- |
| `pydantic_ai_intro.py` | Agent mit strukturierter Ausgabe über ein Pydantic-Modell |
| `pydantic_ai_logfire.py` | derselbe Agent, zusätzlich mit Logfire-Tracing |

## Anpassungen an aktuelle Paketversionen

| vorher | jetzt | Grund |
| --- | --- | --- |
| `Agent(result_type=...)` | `Agent(output_type=...)` | `result_type` wurde in pydantic-ai 2.0 entfernt |
| `result.data` | `result.output` | Umbenennung in pydantic-ai 2.0 |
| `"gpt-4o-mini"` | `"openai:gpt-5.6-luna"` | ohne Provider-Präfix wirft pydantic-ai 2.0 einen `UserError` |
| `logfire.configure()` | zusätzlich `logfire.instrument_pydantic_ai()` | `configure()` instrumentiert pydantic-ai nicht mehr automatisch |
| `import nest_asyncio` | `import nest_asyncio2` | `nest_asyncio` wird nicht mehr gepflegt |
| `from langchain.document_loaders import ...` | `from langchain_classic.document_loaders import ...` | Modul-Split in LangChain 1.0 |
| — | `wikipedia.set_user_agent(...)` + `set_rate_limiting(True)` | siehe unten |

## Wikipedia: `JSONDecodeError` beim Laden

Wikimedia verlangt einen User-Agent **mit Kontaktangabe** (URL oder E-Mail). Der fest
eingebaute User-Agent des Pakets `wikipedia` erfüllt das nicht, die API antwortet dann mit
`429 Too Many Requests`. Da `wikipedia._wiki_request()` den Statuscode nicht prüft und direkt
`r.json()` aufruft, kommt der Fehler als `requests.exceptions.JSONDecodeError` an — oft erst
mitten im Laden, z. B. in `wiki_page.sections`.

Gemessen mit je vier Aufrufen:

| User-Agent | Antworten |
| --- | --- |
| `GenerativeKI-Buch/2.0 (Lernbeispiel)` | `429, 429, 429, 429` |
| `GenerativeKI-Buch/2.0 (https://github.com/...)` | `200, 200, 200, 200` |

Deshalb setzen beide Skripte vor dem Laden einen User-Agent mit Repo-URL und aktivieren
zusätzlich `wikipedia.set_rate_limiting(True)`.

Nebenbei: `load_all_available_meta=True` löst pro Artikel etliche zusätzliche API-Aufrufe aus
(`sections`, `links`, `categories`, …). Die Skripte verwenden nur `page_content` — mit
`load_all_available_meta=False` wird das Laden deutlich schneller und schont das Rate-Limit.
