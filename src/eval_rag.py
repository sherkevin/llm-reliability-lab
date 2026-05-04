import argparse
import json
from pathlib import Path


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def evaluate_retrieval(samples, ks):
    totals = {k: {"hit": 0, "recall": 0.0} for k in ks}
    mrr_sum = 0.0

    for sample in samples:
        gold = set(sample["gold_evidence_ids"])
        retrieved = sample["retrieved_chunk_ids"]

        first_rank = None
        for rank, chunk_id in enumerate(retrieved, start=1):
            if chunk_id in gold:
                first_rank = rank
                break

        if first_rank is not None:
            mrr_sum += 1.0 / first_rank

        for k in ks:
            topk = set(retrieved[:k])
            hits = topk & gold
            totals[k]["hit"] += int(bool(hits))
            totals[k]["recall"] += len(hits) / max(len(gold), 1)

    n = max(len(samples), 1)
    metrics = {"MRR": mrr_sum / n}
    for k in ks:
        metrics[f"HitRate@{k}"] = totals[k]["hit"] / n
        metrics[f"Recall@{k}"] = totals[k]["recall"] / n
    return metrics


def evaluate_citations(samples):
    supported_citations = 0
    total_citations = 0
    supported_claims = 0
    total_claims = 0

    for sample in samples:
        cited = set(sample.get("cited_chunk_ids", []))
        for claim in sample.get("key_claims", []):
            support = set(claim.get("supported_by", []))
            total_claims += 1
            if cited & support:
                supported_claims += 1
            for chunk_id in cited:
                total_citations += 1
                if chunk_id in support:
                    supported_citations += 1

    return {
        "CitationPrecision": supported_citations / max(total_citations, 1),
        "ClaimSupport": supported_claims / max(total_claims, 1),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--k", nargs="+", type=int, default=[1, 3, 5])
    args = parser.parse_args()

    samples = list(load_jsonl(args.data))
    metrics = evaluate_retrieval(samples, args.k)
    metrics.update(evaluate_citations(samples))
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
