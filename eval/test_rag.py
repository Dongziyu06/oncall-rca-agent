"""Quantitative RAG evaluation (Recall@k and MRR)."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.retriever import retrieve


def load_dataset() -> list[dict]:
    path = Path(__file__).with_name("rag_eval_dataset.json")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def evaluate(samples: list[dict], top_k: int) -> tuple[list[dict], float, float]:
    rows = []
    for sample in samples:
        results = retrieve(sample["query"], top_k=top_k) or []
        ids = [str(item.get("id", "")) for item in results]
        expected = set(sample.get("expected_ids", []))
        rank = next((i + 1 for i, ident in enumerate(ids) if ident in expected), None)
        rows.append({
            "query": sample["query"],
            "fault_type": sample.get("fault_type", "unknown"),
            "top_ids": ids,
            "hit": rank is not None,
            "rank": rank,
        })
    total = len(rows) or 1
    recall = sum(row["hit"] for row in rows) / total
    mrr = sum((1.0 / row["rank"]) if row["rank"] else 0.0 for row in rows) / total
    return rows, recall, mrr


def print_table(rows: list[dict], verbose: bool) -> None:
    headers = ["#", "Fault", "Query", "Top-k IDs", "Hit", "Rank"]
    table = []
    for i, row in enumerate(rows, 1):
        query = row["query"] if verbose else (row["query"][:54] + "…" if len(row["query"]) > 55 else row["query"])
        table.append([i, row["fault_type"], query, ", ".join(row["top_ids"]), "Y" if row["hit"] else "N", row["rank"] or "-"])
    try:
        from tabulate import tabulate
        print(tabulate(table, headers=headers, tablefmt="github"))
    except Exception:
        print(" | ".join(headers))
        for values in table:
            print(" | ".join(map(str, values)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Runbook RAG retrieval")
    parser.add_argument("--top-k", type=int, default=3, help="number of retrieved documents (default: 3)")
    parser.add_argument("--verbose", action="store_true", help="print full query details")
    args = parser.parse_args()
    if args.top_k < 1:
        parser.error("--top-k must be >= 1")
    samples = load_dataset()
    rows, recall, mrr = evaluate(samples, args.top_k)
    print_table(rows, args.verbose)
    print(f"\nSummary (k={args.top_k})")
    print(f"Recall@{args.top_k} = {recall:.1%}")
    print(f"MRR = {mrr:.2f}")
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["fault_type"]].append(row)
    print("By fault_type:")
    for fault_type in sorted(grouped):
        group = grouped[fault_type]
        rate = sum(r["hit"] for r in group) / len(group)
        print(f"  {fault_type}: {sum(r['hit'] for r in group)}/{len(group)} ({rate:.1%})")


if __name__ == "__main__":
    main()
