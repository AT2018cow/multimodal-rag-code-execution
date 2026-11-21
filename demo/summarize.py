#!/usr/bin/env python3
"""Turn a demo Q&A .jsonl file into a Markdown summary."""
import argparse
import json
import os
import statistics
from collections import Counter, defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("--out", default=None)
    ap.add_argument("--examples", type=int, default=8)
    args = ap.parse_args()

    recs = [json.loads(line) for line in open(args.jsonl, encoding="utf-8") if line.strip()]
    ok = [r for r in recs if "error" not in r]
    err = [r for r in recs if "error" in r]

    by_paper = Counter(r.get("paper") for r in ok)
    lat = [r["elapsed_s"] for r in ok if r.get("elapsed_s")]
    refs = [len(r.get("references") or []) for r in ok]

    lines = []
    lines.append(f"# Demo Q&A summary — {os.path.basename(args.jsonl)}")
    lines.append("")
    lines.append(f"- records: **{len(recs)}** (ok {len(ok)}, error {len(err)})")
    if lat:
        lines.append(
            f"- latency: mean **{statistics.mean(lat):.1f}s**, "
            f"median **{statistics.median(lat):.1f}s**, max **{max(lat):.1f}s**"
        )
    if refs:
        lines.append(f"- references per answer: mean **{statistics.mean(refs):.1f}**")
    lines.append("")
    lines.append("## Questions per paper")
    lines.append("")
    lines.append("| Paper | Questions |")
    lines.append("|---|---:|")
    for p, n in by_paper.most_common():
        lines.append(f"| {p} | {n} |")
    lines.append("")

    lines.append(f"## Example answers ({args.examples})")
    lines.append("")
    for r in ok[: args.examples]:
        lines.append(f"### {r['question']}")
        lines.append("")
        answer = (r.get("answer") or "").strip()
        lines.append(answer[:1200] + ("…" if len(answer) > 1200 else ""))
        lines.append("")

    if err:
        lines.append("## Errors")
        lines.append("")
        for r in err[:20]:
            lines.append(f"- `{r['question'][:80]}` — {r.get('error', '')[:160]}")
        lines.append("")

    out = args.out or args.jsonl.replace(".jsonl", "_summary.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
