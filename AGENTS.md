# AGENTS.md

## What this is

Azure-based multimodal RAG accelerator ("Research CoPilot"): ingest PDF/DOCX/XLSX (text, images, tables) into AI Search, chat via Chainlit/Streamlit with code execution (OpenAI Assistants API, optional TaskWeaver). Python 3.10 (conda env `mmdoc`). No pyproject/lint/test config exists; there are no automated tests.

This fork's Azure deployment carries substantial **out-of-band state** (access restrictions, Entra auth, private endpoints, keyless data-plane auth, Key Vault references) that a bicep re-provision will NOT recreate. Before any infrastructure work, read `deployment/OPERATIONS.md` — it documents the deployment state, the endpoint inventory, and the full re-apply checklist.

## Repo layout

- `code/` — backend. FastAPI app in `api.py` (single module, all routes). Ingestion pipeline in `processor.py` + `ingest_doc.py` (CLI taking `--ingestion_params_dict '<json>'`). `doc_utils.py` = search/generation logic. `utils/` = Azure service helpers. `code/prompts/*.txt` = all LLM prompt templates, loaded at runtime (change prompts here, not in code).
- `ui/` — `chat.py` (Chainlit chat app), `main.py` + `pages/` (Streamlit multipage: Prompt Management, Ingestion). `ui/experiments/` is scratch, not production.
- `code/processing_plan.json` — defines per-file-format processing pipelines (lists of function names run in order by `Processor`). Modifying ingestion behavior usually means editing this, not the Python.
- `docker/` — Dockerfiles for api/chainlit/streamlit apps. `deployment/` — Bicep + PowerShell deploy scripts + `OPERATIONS.md` (deployment runbook for this fork).

## Running locally

Requires `.env` at repo root (copy `.env.sample`; strictly no spaces/quotes around values). All three apps call `load_dotenv(override=True)` from the repo root.

The API must start first (port 9000; `API_BASE_URL=http://localhost:9000` for local runs):

```bash
pip install -r code/requirements.txt   # README mentions a root requirements.txt; it does not exist
pip install -r ui/requirements.txt     # only if running the UIs

cd code && python -m uvicorn api:app --reload --port 9000
cd ui && chainlit run chat.py          # chat app
cd ui && streamlit run main.py         # ingestion + prompt management
```

`invoke start-api|start_chat|start_main` (see `tasks.py`) wrap these, but use `&` instead of `&&` for `cd`, so prefer running the commands directly.

## Code & build invariants

- `code/` modules import each other flat (`from doc_utils import *`, `from utils.x import ...`) and expect to be run from inside `code/` (or with `PYTHONPATH` including `code/`, as set in `.env.sample`). `processor.py` has try/except imports for both layouts.
- Everything depends on Azure services (OpenAI, AI Search, Cosmos, Document Intelligence, Storage, optionally AML) — no offline mode. Notebooks in `tutorials/` are the fastest way to exercise a single concept; `tutorials/requirements.txt` is separate.
- TaskWeaver and AutoGen are optional: TaskWeaver needs its repo cloned, `test_project/` dir, and `taskweaver_config.json` (from `taskweaver_config.sample.json`). AutoGen notebooks need `code/OAI_CONFIG_LIST` (from `OAI_CONFIG_LIST.sample`).
- `.env.sample` has duplicate AML/storage sections (later values win) and multiple numbered `AZURE_OPENAI_RESOURCE_N`/`KEY_N` pools for multi-threaded ingestion.
- Deployment: `.github/workflows/deploy.yml` is manual-dispatch only (Bicep via az CLI). `deployment/push.ps1` builds/pushes only Docker images to ACR; web apps must then be manually repointed in the Portal.
- `gpt-5.6-luna` (current chat/vision model, on the writic-resource Foundry account) is a reasoning model: it rejects `temperature` (any non-default) and `max_tokens` (use `max_completion_tokens`). `code/utils/openai_utils.py` is patched accordingly; **don't reintroduce those params**. Verified-compatible data-plane api-version: `2024-10-21` for chat/vision, `2023-12-01-preview` for embeddings.
- Data-plane auth is dual-mode: when `AZURE_CLIENT_ID` is set (prod) all data-service calls use Entra tokens via `env_vars.get_entra_credential()/get_entra_token()/search_auth_headers()`; when unset (local dev) they fall back to key auth. Preserve this duality when touching auth code.
- `/models` in `code/api.py` masks AOAI keys — never return secrets to clients.
- Container-image build gotchas: `python:3.10-slim` is now Debian trixie (Ubuntu-only apt packages break Dockerfiles — `software-properties-common` was removed from dockerfile_streamlit_app); `pydantic` must stay `<2.10` for chainlit 1.0.502 (`CodeSettings is not fully defined` crash); failed deploymentScripts are not re-run on redeploy unless deleted first (`az resource delete --resource-type Microsoft.Resources/deploymentScripts -n <name>`).

## Docs

- `README.md` — main doc: pipeline concept, run instructions, per-step function reference.
- `ENTERPRISE_DEPLOYMENT.md`, `deployment/README.md` — Azure deployment details.
- `deployment/OPERATIONS.md` — this fork's deployment state, endpoint inventory, costs, and the re-provision checklist.
- `deployment/SERVICE_INVENTORY.md` — complete service table with configuration, verified unit prices, and MfS milestone workload floors.
