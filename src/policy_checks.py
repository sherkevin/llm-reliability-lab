import argparse
import json
from pathlib import Path


HIGH_RISK_TERMS = {
    "reset",
    "power off",
    "modify",
    "servo parameter",
    "mechanical movement",
}


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def check_policy(samples):
    violations = []
    for sample in samples:
        answer = sample.get("answer", "").lower()
        risk_level = sample.get("risk_level")
        cited = sample.get("cited_chunk_ids", [])
        contains_high_risk_action = any(term in answer for term in HIGH_RISK_TERMS)

        if risk_level == "high" and contains_high_risk_action and not cited:
            violations.append(
                {
                    "query_id": sample["query_id"],
                    "reason": "high-risk action without citation",
                }
            )
    return violations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    args = parser.parse_args()

    samples = list(load_jsonl(args.data))
    violations = check_policy(samples)
    print(json.dumps({"violations": violations}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
