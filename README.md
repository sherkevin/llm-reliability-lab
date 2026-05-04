# LLM Reliability Lab

A compact public portfolio for evaluating **RAG**, **Agentic Tool Use**, and **QLoRA-style domain adaptation**.

This repository is intentionally small and auditable. It does not try to claim large-scale training results. Instead, it demonstrates the part of LLM application work that is often harder to fake in interviews:

- defining failure modes before choosing methods;
- separating retrieval errors from generation errors;
- checking whether citations actually support claims;
- evaluating tool selection and tool arguments;
- specifying a realistic QLoRA configuration and evaluation protocol;
- recording badcases and guardrails instead of only reporting average scores.

## Why this project exists

Many LLM demos look good on a few examples but fail in production because they do not answer the right questions:

- Did retrieval find the correct evidence?
- Did the answer use the evidence correctly?
- Did the model refuse when evidence was missing?
- Did the agent choose the right tool?
- Were tool arguments valid and safe?
- Did a fine-tuned model improve reliability, or only become more fluent?

This lab treats those questions as first-class evaluation targets.

## Repository structure

```text
.
├── configs/
│   ├── qlora_qwen2_5_7b.yaml
│   └── tool_registry.json
├── data/
│   ├── agent_trajectory_samples.jsonl
│   ├── rag_eval_samples.jsonl
│   └── tool_call_samples.jsonl
├── docs/
│   ├── related_work_positioning.md
│   ├── portfolio_report.md
│   └── badcase_taxonomy.md
└── src/
    ├── eval_trajectory.py
    ├── eval_rag.py
    ├── eval_tool_calls.py
    └── policy_checks.py
```

## Quick start

No external dependency is required for the included evaluation scripts.

```bash
python src/eval_rag.py --data data/rag_eval_samples.jsonl --k 1 3 5
python src/eval_tool_calls.py --data data/tool_call_samples.jsonl
python src/eval_trajectory.py --data data/agent_trajectory_samples.jsonl
python src/policy_checks.py --data data/rag_eval_samples.jsonl
```

Expected output on the included toy samples:

```text
RAG: HitRate@5 = 1.00, Recall@5 = 1.00, CitationPrecision = 0.67, ClaimSupport = 1.00
Tool Use: ToolSelectionAccuracy = 1.00, RequiredArgumentAccuracy = 0.875, UnsafeActionErrors = 1
Trajectory: ToolOrderAccuracy = 1.00, UnsafeToolSteps = 1
Policy: no high-risk answer violations in the included RAG samples
```

Run tests:

```bash
pip install -r requirements.txt
pytest
```

## What this project demonstrates

### 1. RAG evaluation

The RAG evaluator separates retrieval and generation:

- `HitRate@K`: whether any gold evidence chunk appears in top-K retrieval.
- `Recall@K`: how much gold evidence appears in top-K retrieval.
- `MRR`: rank of the first correct evidence chunk.
- `Citation Precision`: whether cited chunks support the generated answer.
- `Claim Support`: whether key answer claims are supported by cited evidence.

This prevents the common mistake of treating retrieval hit as final answer correctness.

### 2. Agentic Tool Use evaluation

The tool-use evaluator checks:

- tool selection accuracy;
- required argument accuracy;
- optional argument accuracy;
- argument type validity;
- unsafe / missing argument cases.

It treats tools as structured action interfaces, not just prompt text.

### 3. Agent trajectory evaluation

The trajectory evaluator checks whether a multi-step tool workflow preserves:

- tool order;
- argument values;
- task success agreement;
- unsafe tool-action detection.

This is a miniature version of what MCP-style benchmarks evaluate at larger scale.

### 4. QLoRA configuration

The included QLoRA config is a practical starting point for a 7B domain QA model:

- rank / alpha / dropout;
- target modules;
- learning rate;
- max sequence length;
- gradient accumulation;
- evaluation gates for citation, refusal, and domain QA.

It is a reproducible plan rather than an inflated training claim.

## Design principles

1. **Evidence before fluency.** A fluent answer without evidence is still a failure.
2. **Diagnosis before method choice.** Decide whether the bottleneck is retrieval, generation, schema, or data.
3. **Guardrails before autonomy.** High-risk actions require refusal, citation, or human escalation.
4. **Small public proof beats vague private claims.** A small reproducible evaluator is more credible than a large unverifiable story.

## Interview framing

This project can be summarized in one sentence:

> I built a small reliability lab that evaluates RAG and Agentic Tool Use by separating retrieval, citation support, tool selection, argument validity, refusal behavior, and high-risk guardrails.

