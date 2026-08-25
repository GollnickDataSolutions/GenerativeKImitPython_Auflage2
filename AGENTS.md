# AGENTS.md

German book repo ("Generative KI mit Python", 2. Auflage, Rheinwerk). It is a set of runnable
examples, not a library/app. Code and prose are authored together: each `Code/<chapter>` mirrors a
chapter draft under `Entwurf/` (`.docx`/`.pptx`/images). Prefer code as source of truth; `README.md`
is empty.

## Toolchain
- Python 3.13, managed with **uv** (`pyproject.toml` + `uv.lock` at repo root).
- Main env is `.venv` — sync with `uv sync`, run scripts with `.venv\Scripts\python.exe`.
- **Separate env `.venv-ragas` is required for `Code/07_RAG/60_rag_eval.py`** because ragas 0.4.x and
  `langchain-experimental` (SemanticChunker, ch06) need conflicting `langchain-community` versions.
  See `Code/07_RAG/requirements_ragas.txt` for the reason + setup. Run with:
  `uv run --python .venv-ragas Code/07_RAG/60_rag_eval.py`.
- No test framework, no CI/lint/typecheck/pre-commit config. Verification = run the numbered script.

## API keys (.env)
- Keys live in the repo-root `.env`: `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `TAVILY_API_KEY`,
  `PINECONE_API_KEY`, `AGENTOPS_API_KEY`. Some chapter dirs have their own `.env` (`Code/07_RAG/.env`).
- Scripts load it via `load_dotenv(find_dotenv(usecwd=True))`/`load_dotenv()`, so **run scripts from the
  repo root** (or a dir whose `.env` is reachable), not from inside a chapter folder, or keys won't load.

## Conventions
- Example files are named `NN_name.py` with a leading number; preserve numbering and the `#%%` cell
  markers (VSCode Jupyter-style interactive cells).
- **Cross-chapter imports**: e.g. `07_RAG/10_simple_RAG.py` does `sys.path.append(...)` to
  `../06_VectorDatabases/10_DataLoader` to import `loaders.py` (`WikipediaLoader`). Keep these paths intact.
- Framework version quirks — do NOT "modernize"/revert:
  - langchain **1.x**; langchain_* packages (`langchain_openai`, `langchain_openrouter`, ...).
  - transformers **5.x**: the `"summarization"` pipeline is gone (ch03 loads the seq2seq model directly).
  - SemanticChunker in ch06 needs `langchain-experimental`.
- Heavier runtime: ch03/08 download HF models; ch11 sub-projects have their own deps
  (`11_Deployment/streamlit` has its own `requirements.txt` and a nested `.git`; `rest_api` uses fastapi+uvicorn).
- `.claude/skills/` (powerpoint, brand-guidelines) belong to a different project (Tokenomics wiki) — ignore, not related to the book.
