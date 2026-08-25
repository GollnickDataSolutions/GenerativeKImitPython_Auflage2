#%% packages
from dotenv import load_dotenv 
from langchain_openrouter import ChatOpenRouter
import os
import sys
import time
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "06_VectorDatabases","10_DataLoader"
    )
)
from loaders import TextLoader
from rich.console import Console
from rich.table import Table
console = Console()
load_dotenv()


#%% Konfiguration
MODEL_NAME = "anthropic/claude-haiku-4.5"
CONTEXT_CHARS = 40_000
MAX_TOKENS = 300
model = ChatOpenRouter(model=MODEL_NAME, max_tokens=MAX_TOKENS)

SYSTEM_INSTRUCTION = (
    "Du bist ein Literaturexperte. Beantworte Fragen ausschließlich auf Basis des folgenden Romanausschnitts. Antworte in höchstens zwei Sätzen."
)

QUESTIONS = [
    "Wer erzählt die Geschichte?",
    "Welche Rolle spielt Dr. Mortimer?",
    "Was hat es mit dem Hund auf sich?",
]

#%% Kontext laden
data_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "06_VectorDatabases", "data"
)
doc = TextLoader(file_path=os.path.join(data_dir, "HoundOfBaskerville.txt")).load()
context_text = doc[0].page_content[:CONTEXT_CHARS]
console.print(f"Kontext: {len(context_text):,} Zeichen")

#%% Modell
# OpenRouter liefert die tatsaechlich abgerechneten Kosten jedes Aufrufs mit.
# Sie stehen anschliessend in response.response_metadata["cost"].

#%% Nachrichten bauen
def build_system_message(use_cache: bool) -> dict:
    """Systemnachricht mit dem langen Kontext, optional mit Cache-Breakpoint.
    """
    context_block = {"type": "text", "text": context_text}
    if use_cache:
        context_block["cache_control"] = {"type": "ephemeral"}
    return {
        "role": "system",
        "content": [
            {"type": "text", "text": SYSTEM_INSTRUCTION},
            context_block,
        ],
    }

#%% Ein mehrstufiges Gespraech fuehren und dabei messen
def run_conversation(use_cache: bool) -> list[dict]:
    """Stellt alle Fragen nacheinander im selben Gespraech.
    """
    messages = [build_system_message(use_cache)]
    stats = []

    for question in QUESTIONS:
        messages.append({"role": "user", "content": question})

        start = time.perf_counter()
        response = model.invoke(messages)
        duration = time.perf_counter() - start

        messages.append({"role": "assistant", "content": response.content})

        usage = response.usage_metadata or {}
        details = usage.get("input_token_details") or {}
        stats.append({
            "frage": question,
            "dauer": duration,
            "input": usage.get("input_tokens", 0),
            "cache_write": details.get("cache_creation", 0),
            "cache_read": details.get("cache_read", 0),
            "output": usage.get("output_tokens", 0),
            "kosten": response.response_metadata.get("cost"),
        })

    return stats

#%% Durchlauf A: ohne Caching
stats_ohne_cache = run_conversation(use_cache=False)

#%% Durchlauf B: mit Caching
# Wichtig: direkt im Anschluss ausfuehren, der Cache lebt nur 5 Minuten.
# Hinweis: Wird das Skript innerhalb dieser 5 Minuten erneut gestartet, ist der
# Cache noch gefuellt. Dann zeigt schon die erste Zeile einen Cache-Read statt
# eines Cache-Writes - die Ersparnis faellt entsprechend noch groesser aus.
stats_mit_cache = run_conversation(use_cache=True)

#%% Ergebnisse als Tabelle
def show_table(title: str, stats: list[dict]) -> None:
    table = Table(title=title)
    table.add_column("Frage", no_wrap=True, overflow="ellipsis", max_width=24)
    table.add_column("Sek.", justify="right")
    table.add_column("Input", justify="right")
    table.add_column("Write", justify="right")
    table.add_column("Read", justify="right")
    table.add_column("Out", justify="right")
    table.add_column("USD", justify="right")

    for i, row in enumerate(stats, start=1):
        kosten = f"{row['kosten']:.6f}" if row["kosten"] is not None else "–"
        table.add_row(
            f"{i}. {row['frage']}",
            f"{row['dauer']:.0f}",
            f"{row['input']:,}",
            f"{row['cache_write']:,}",
            f"{row['cache_read']:,}",
            f"{row['output']:,}",
            kosten,
        )

    console.print(table)

show_table("Ohne Prompt Caching", stats_ohne_cache)
show_table("Mit Prompt Caching", stats_mit_cache)

#%% Auswertung
def summe(stats: list[dict], key: str) -> float:
    return sum(row[key] or 0 for row in stats)

kosten_ohne = summe(stats_ohne_cache, "kosten")
kosten_mit = summe(stats_mit_cache, "kosten")
dauer_ohne = summe(stats_ohne_cache, "dauer")
dauer_mit = summe(stats_mit_cache, "dauer")
gelesen = summe(stats_mit_cache, "cache_read")

console.print(f"\nAus dem Cache gelesene Token: {gelesen:,.0f}")
console.print(f"Dauer:  {dauer_ohne:.1f} s  ->  {dauer_mit:.1f} s")

if kosten_ohne and kosten_mit:
    ersparnis = (1 - kosten_mit / kosten_ohne) * 100
    console.print(f"Kosten: {kosten_ohne:.6f} USD  ->  {kosten_mit:.6f} USD")
    console.print(f"Ersparnis über {len(QUESTIONS)} Fragen: {ersparnis:.1f} %")
else:
    console.print("Keine Kostendaten erhalten - liefert OpenRouter 'usage.cost' zurück?")

