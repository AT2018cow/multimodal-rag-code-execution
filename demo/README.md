# Demo traffic

Synthetic-but-realistic usage of the Research CoPilot for demos.

## What is here

| File | Purpose |
|---|---|
| `questions.json` | 90 questions: 10 per arXiv paper + 10 cross-paper questions |
| `run_demo_traffic.py` | Calls `POST /search-stream` for each question and appends results to JSONL |
| `qa_<index>_<date>.jsonl` | Generated Q&A records (question, answer, references, latency) |

The demo corpus is 8 open-access arXiv papers on retrieval-augmented generation,
ingested into the `demo-rag-2026` index:

| arXiv | Title |
|---|---|
| 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks |
| 2312.10997 | Retrieval-Augmented Generation for Large Language Models: A Survey |
| 2112.04426 | Improving language models by retrieving from trillions of tokens |
| 2208.03299 | Atlas: Few-shot Learning with Retrieval Augmented Language Models |
| 2211.12561 | Retrieval-Augmented Multimodal Language Modeling |
| 2310.11511 | Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection |
| 2404.16130 | From Local to Global: A Graph RAG Approach to Query-Focused Summarization |
| 2401.15884 | Corrective Retrieval Augmented Generation |

The papers are public (arXiv) and are used only as demo content; nothing here is
confidential.

## Running

The API is behind IP allow-listing and Entra ID auth, so run this from a host
whose IP is allowed (the proxy VM is) and provide the backend
client credentials.

On the admin workstation they are kept in `~/.config/research-copilot/api.env`
(chmod 600, never committed):

```bash
set -a; source ~/.config/research-copilot/api.env; set +a
python run_demo_traffic.py --index demo-rag-2026 --limit 90 --workers 2
```

Or export them explicitly:

```bash
export API_BASE_URL=https://dev-app-api-<suffix>.azurewebsites.net
export API_AUTH_TENANT_ID=<tenant id>
export API_AUTH_CLIENT_ID=<copilot-backends app id>
export API_AUTH_CLIENT_SECRET=<client secret>
export API_AUTH_SCOPE=api://<api app id>/.default

python run_demo_traffic.py --index demo-rag-2026 --limit 90 --workers 2
```

`--limit 0` runs all 90 questions. Each run appends to a new dated JSONL file, so
daily runs accumulate history without overwriting.

## Cost

Each question costs roughly 10–20k prompt tokens plus one Assistants API call.
90 questions is on the order of $0.3–0.6 at current `gpt-5.6-luna` pricing.
Ingestion of the 8 papers is a one-time ~$2–3 (Document Intelligence + chunk
tagging + embeddings).
