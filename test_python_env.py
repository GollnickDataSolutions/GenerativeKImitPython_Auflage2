"""Prüft, ob die Python-Umgebung für dieses Buch korrekt eingerichtet ist.

Aufruf:
    python test_python_env.py

Geprüft wird:
1. Python-Version (>= 3.13)
2. Verwendeter Python-Interpreter (virtuelle Umgebung aktiv?)
3. Wichtigste Pakete installiert
"""

#%% packages
import importlib
import importlib.metadata as metadata
import sys

#%% Konfiguration
MIN_PYTHON = (3, 13)

# (Import-Name, Paketname auf PyPI)
REQUIRED_PACKAGES = [
    ("openai", "openai"),
    ("dotenv", "python-dotenv"),
    ("langchain_openai", "langchain-openai"),
    ("langchain_openrouter", "langchain-openrouter"),
    ("langchain_ollama", "langchain-ollama"),
    ("transformers", "transformers"),
    ("torch", "torch"),
    ("accelerate", "accelerate"),
    ("mcp", "mcp"),
    ("agent_framework", "agent-framework-core"),
    ("agent_framework_openai", "agent-framework-openai"),
    ("agent_framework_orchestrations", "agent-framework-orchestrations"),
    ("ipykernel", "ipykernel"),
]

OK = "[  OK  ]"
FAIL = "[FEHLER]"
WARN = "[ WARN ]"


def abschnitt(titel: str) -> None:
    print(f"\n{titel}")
    print("-" * len(titel))


#%% 1. Python-Version
def pruefe_python_version() -> bool:
    abschnitt("1. Python-Version")
    version = ".".join(str(t) for t in sys.version_info[:3])
    erwartet = ".".join(str(t) for t in MIN_PYTHON)

    if sys.version_info >= MIN_PYTHON:
        print(f"{OK} Python {version} (benötigt: >= {erwartet})")
        return True

    print(f"{FAIL} Python {version} ist zu alt (benötigt: >= {erwartet}).")
    print("         Installieren Sie eine aktuelle Python-Version von python.org.")
    return False


#%% 2. Virtuelle Umgebung
def pruefe_umgebung() -> bool:
    abschnitt("2. Virtuelle Umgebung")
    print(f"         Interpreter: {sys.executable}")

    # In einer virtuellen Umgebung weicht sys.prefix von sys.base_prefix ab.
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        print(f"{OK} Virtuelle Umgebung ist aktiv ({sys.prefix}).")
        return True

    print(f"{WARN} Es ist keine virtuelle Umgebung aktiv.")
    print("         Aktivieren Sie sie mit:")
    print("           Windows: .venv\\Scripts\\activate")
    print("           macOS/Linux: source .venv/bin/activate")
    return False


#%% 3. Pakete
def pruefe_pakete() -> bool:
    abschnitt("3. Wichtigste Pakete")
    fehlend = []

    for import_name, paket_name in REQUIRED_PACKAGES:
        try:
            importlib.import_module(import_name)
        except ImportError:
            print(f"{FAIL} {paket_name:<22} nicht installiert")
            fehlend.append(paket_name)
            continue

        try:
            version = metadata.version(paket_name)
        except metadata.PackageNotFoundError:
            version = "unbekannt"
        print(f"{OK} {paket_name:<22} {version}")

    if fehlend:
        print("\n         Nachinstallieren mit:")
        print(f"           uv sync   (oder: pip install {' '.join(fehlend)})")
        return False
    return True


#%% main
def main() -> int:
    print("=" * 60)
    print("Prüfung der Python-Umgebung für 'Generative KI mit Python'")
    print("=" * 60)

    version_ok = pruefe_python_version()
    venv_ok = pruefe_umgebung()
    pakete_ok = pruefe_pakete()

    abschnitt("Zusammenfassung")
    # Nur Version und Pakete sind zwingend; die virtuelle Umgebung ist ein Hinweis.
    kritisch_ok = version_ok and pakete_ok

    if kritisch_ok and venv_ok:
        print("Alles bereit – Sie können mit den Beispielen des Buches starten.")
        return 0

    if kritisch_ok:
        print("Alle Pakete sind vorhanden, beachten Sie aber die Hinweise (WARN) oben.")
        return 0

    print("Die Umgebung ist noch nicht einsatzbereit. Bitte die mit FEHLER")
    print("markierten Punkte oben beheben.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
