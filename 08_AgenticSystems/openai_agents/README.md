# OpenAI Agents SDK

Beispiele zum [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) (Version 0.19.x).

## Eigene Umgebung

Diese Beispiele laufen **nicht** in der Umgebung des Hauptprojekts: `openai-agents` benötigt
`mcp<2`, Kapitel 9 (MCP) dagegen `mcp>=2`. Deshalb hat dieser Ordner ein eigenes `pyproject.toml`:

```bash
cd Code/08_AgenticSystems/openai_agents
uv sync
```

In VS Code anschließend `Code/08_AgenticSystems/openai_agents/.venv` als Interpreter auswählen.

Der `OPENAI_API_KEY` wird aus der `.env` im Projekt-Hauptverzeichnis geladen.

## Skripte

| Skript | Inhalt |
| --- | --- |
| `agents_single_agent.py` | einzelner Agent mit `Agent` und `Runner` |
| `agents_multiple_agents.py` | Triage-Agent mit Handoffs an spezialisierte Agenten |
| `agents_tools.py` | Agent mit eigenen Tools (`@function_tool`) über Wikipedia |
