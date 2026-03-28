# CodeTablet — Run Instructions

This repository is an agent-based project generator. It contains:

- a FastAPI backend that runs the agent pipeline and streams events: [fastapi_app/api_main.py](fastapi_app/api_main.py#L1)
- a local Streamlit frontend that runs the agent in-process: [mmain.py](mmain.py)
- a Streamlit frontend that calls an HTTP build API (remote by default): [main.py](main.py)
- agent implementation: [agent/](agent)
- example generated project(s): [generated_project/](generated_project) and timestamped snapshots like [generated_project_20260219_195822/](generated_project_20260219_195822)

This README explains how to run each component separately and how they interact.

Prerequisites
- Python 3.10+ (3.11 recommended)
- Git (optional, for cloning)

Quick setup (cross-platform)

Windows PowerShell

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Environment variables / credentials

Create a `.env` file in the repo root or set environment variables in your shell. The project uses LLM adapters and may require provider credentials depending on which connector you use:

- `OPENAI_API_KEY` — set when using `langchain_openai` (ChatOpenAI).
- `OLLAMA_*` — variables used if you switch to an Ollama adapter.

Where configuration lives in code

- The in-process Streamlit UI is `mmain.py`. It imports the agent from `agent.graph` and runs the pipeline locally.
- The remote-style Streamlit UI is `main.py`. It calls the API at `API_URL` built from the `EC2_IP` variable inside the file — change it to `127.0.0.1` to point to a local API instance.
- The FastAPI app is in [fastapi_app/api_main.py](fastapi_app/api_main.py#L1) and mounts routes from [fastapi_app/routes.py](fastapi_app/routes.py#L1).

Running components separately

1) Start the FastAPI backend (serves build stream and download)

```powershell
uvicorn fastapi_app.api_main:app --reload --port 8000
```

- Endpoint overview:
  - `GET /` — health info
  - `POST /build/stream` — start a build and stream Server-Sent Events from the agent
  - `GET /download?project_name=<name>` — download a ZIP of the generated project (router uses `project_name`)

2) Run the local Streamlit UI (in-process agent)

```powershell
streamlit run mmain.py
```

- `mmain.py` runs the agent graph directly in your Python process. It requires LLM credentials available to the environment and will write generated projects under a timestamped `generated_project_YYYYMMDD_HHMMSS` folder (created by the agent tools).

3) Run the Streamlit UI that calls the API

```powershell
streamlit run main.py
```

- `main.py` is intended to call a remote API defined by `EC2_IP` at the top of the file. If you are running the FastAPI backend locally, update `EC2_IP = "127.0.0.1"` inside `main.py` so the UI calls your local server.

Typical workflow

1. Start the FastAPI backend (if you want a server-based build).
2. Start the Streamlit UI you prefer (`mmain.py` for local, `main.py` for server+client).
3. Enter a natural-language project description and press "Build"; generated projects are placed in `generated_project_*` timestamped folders.
4. Use the UI download button or call the `/download` endpoint to get a ZIP.

Agent implementation notes

- The agent pipeline is defined in `agent/graph.py` and uses three logical nodes:
  - `planner` — produces a high-level `Plan` (see `agent/states.py`)
  - `architect` — expands the plan into a `TaskPlan` composed of `ImplementationTask` steps
  - `coder` — iterates tasks and writes files using the tools in `agent/tools.py`

- Tools for file IO and sandboxing are in `agent/tools.py`. Generated output is written under the path provided to `set_project_root()` (the FastAPI route sets this to a timestamped folder in the repo root).

Generated example

- `generated_project/` contains a sample calculator project (HTML/CSS/JS) with a `README.md` describing it. Timestamped folders such as `generated_project_20260219_195822/` are previous outputs.

Cleaning and housekeeping

Files you can safely delete (optional):

- Python bytecode caches: `agent/__pycache__/`, `fastapi_app/__pycache__/`
- Old generated snapshots: `generated_project_YYYYMMDD_HHMMSS/` (delete if you don't need them)
- Local virtual environment: `.venv/` — do not commit this; recreate locally with `python -m venv .venv`

Files to keep and review before deletion

- `mmain.py` and `main.py` — they provide different UI modes; keep the one(s) you use.

Notes & troubleshooting

- If Streamlit shows errors about missing modules, ensure `pip install -r requirements.txt` completed successfully inside the activated venv.
- If the agent can't access your LLM, confirm the env vars and that the chosen LLM connector (OpenAI vs Ollama) is installed and configured.
- If `main.py` doesn't connect to the API, change `EC2_IP` to `127.0.0.1` when using a local FastAPI server.

Next steps I can take

- Add a small `scripts/start_all.sh` / `start_all.ps1` to run backend + UI together.
- Remove selected unwanted files (`.venv/`, caches, old generated snapshots) — tell me which to delete and I'll remove them.
