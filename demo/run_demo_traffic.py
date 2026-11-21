#!/usr/bin/env python3
"""
Generate demo Q&A traffic against the Research CoPilot API.

Reads questions from questions.json, calls POST /search-stream, and appends
one JSON record per question to a .jsonl file.

Authentication (client credentials, same app registration the UIs use):
    API_AUTH_TENANT_ID
    API_AUTH_CLIENT_ID
    API_AUTH_CLIENT_SECRET
    API_AUTH_SCOPE          default: api://<API_APP_ID>/.default
    API_BASE_URL            e.g. https://dev-app-api-<suffix>.azurewebsites.net

Usage:
    python run_demo_traffic.py --index demo-rag-2026 --limit 90
    python run_demo_traffic.py --index spark2paper --limit 20 --workers 2

The output file defaults to qa_<index>_<YYYY-MM-DD>.jsonl next to this script.
"""
import argparse
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import requests

TENANT = os.getenv("API_AUTH_TENANT_ID", "")
CLIENT_ID = os.getenv("API_AUTH_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("API_AUTH_CLIENT_SECRET", "")
SCOPE = os.getenv("API_AUTH_SCOPE", "")
BASE = os.getenv("API_BASE_URL", "").rstrip("/")

_token = {"value": None, "expires_at": 0.0}
_lock = threading.Lock()


def token():
    if not (TENANT and CLIENT_ID and CLIENT_SECRET and SCOPE and BASE):
        sys.exit("missing API_AUTH_* / API_BASE_URL environment variables")
    with _lock:
        if _token["value"] and time.time() < _token["expires_at"] - 60:
            return _token["value"]
        r = requests.post(
            f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token",
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "scope": SCOPE,
            },
            timeout=30,
        )
        r.raise_for_status()
        payload = r.json()
        _token["value"] = payload["access_token"]
        _token["expires_at"] = time.time() + payload.get("expires_in", 3600)
        return _token["value"]


def ask(index_name, question, user_id, timeout=600):
    body = {
        "query": question,
        "top": 3,
        "approx_tag_limit": 3,
        "conversation_history": [],
        "user_id": user_id,
        "computation_approach": "AssistantsAPI",
        "computation_decision": "LLM",
        "vision_support": False,
        "include_master_py": True,
        "vector_type": "AISearch",
        "index_name": index_name,
        "full_search_output": True,
        "count": False,
        "token_limit": 100000,
        "temperature": 0.2,
        "verbose": False,
    }
    started = time.time()
    with requests.post(
        f"{BASE}/search-stream",
        json=body,
        headers={"Authorization": f"Bearer {token()}"},
        stream=True,
        timeout=timeout,
    ) as r:
        r.raise_for_status()
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            kind, content = json.loads(line)
            if kind == "RESULT":
                answer, references, output_excel, search_results, files = content
                return {
                    "answer": answer,
                    "references": references,
                    "elapsed_s": round(time.time() - started, 2),
                }
            if kind == "ERROR":
                raise RuntimeError(str(content))
    raise RuntimeError("stream ended without a RESULT frame")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default="demo-rag-2026")
    ap.add_argument("--questions", default=os.path.join(here, "questions.json"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=0, help="0 = all questions")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--pause", type=float, default=0.5, help="seconds between starts")
    args = ap.parse_args()

    with open(args.questions, encoding="utf-8") as f:
        questions = json.load(f)
    if args.limit:
        questions = questions[: args.limit]

    out = args.out or os.path.join(
        here, f"qa_{args.index}_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    )
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    def work(item):
        last = None
        for attempt in range(1, args.retries + 2):
            try:
                res = ask(args.index, item["question"], f"demo-{run_id}")
                return {
                    "run_id": run_id,
                    "index": args.index,
                    "arxiv_id": item.get("arxiv_id"),
                    "paper": item.get("title"),
                    "question": item["question"],
                    "answer": res["answer"],
                    "references": res["references"],
                    "elapsed_s": res["elapsed_s"],
                    "attempt": attempt,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            except Exception as e:  # noqa: BLE001
                last = e
                time.sleep(2 * attempt)
        return {
            "run_id": run_id,
            "index": args.index,
            "arxiv_id": item.get("arxiv_id"),
            "paper": item.get("title"),
            "question": item["question"],
            "error": str(last),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    ok = err = 0
    with open(out, "a", encoding="utf-8") as f, ThreadPoolExecutor(args.workers) as pool:
        futures = []
        for item in questions:
            futures.append(pool.submit(work, item))
            time.sleep(args.pause)
        for fut in as_completed(futures):
            rec = fut.result()
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            if "error" in rec:
                err += 1
                print(f"ERR  {rec['question'][:70]} -> {rec['error'][:120]}")
            else:
                ok += 1
                print(f"OK   {rec['elapsed_s']:6.1f}s  {rec['question'][:80]}")

    print(f"\nwrote {ok + err} records to {out} (ok={ok}, error={err})")


if __name__ == "__main__":
    main()
