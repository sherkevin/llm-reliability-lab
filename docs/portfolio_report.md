# Portfolio Report

## Summary

This project demonstrates a reliability-first workflow for LLM applications.

The core idea is to avoid evaluating an LLM application as a single black box.
Instead, the system is decomposed into:

1. retrieval;
2. citation support;
3. answer faithfulness;
4. refusal behavior;
5. tool selection;
6. tool argument validity;
7. high-risk policy compliance.

## Why average accuracy is not enough

For industrial RAG and Agentic Tool Use, a high average score can hide severe failures:

- retrieval finds the right document, but the answer cites the wrong sentence;
- the answer is fluent, but the claim is unsupported;
- the agent selects the right tool, but sends unsafe arguments;
- the model answers high-risk questions instead of refusing or escalating.

The project therefore separates component-level metrics.

## Evaluation examples

### RAG

The included sample set evaluates:

- fault-code retrieval;
- SOP safety;
- hybrid retrieval for exact IDs and semantic descriptions;
- citation support for key claims.

### Agentic Tool Use

The tool-call sample set evaluates:

- whether the model selects the correct tool;
- whether required arguments match expected values;
- whether high-risk actions are blocked.

## Current toy-sample results

The included samples are intentionally small and readable. They are used to
demonstrate evaluator behavior, not to claim benchmark performance.

```text
RAG evaluator
- MRR: 0.8333
- HitRate@1: 0.6667
- Recall@1: 0.5000
- HitRate@3 / Recall@3: 1.0000
- HitRate@5 / Recall@5: 1.0000
- CitationPrecision: 0.6667
- ClaimSupport: 1.0000

Tool-call evaluator
- ToolSelectionAccuracy: 1.0000
- ArgumentExactMatch: 0.6667
- RequiredArgumentAccuracy: 0.8750
- UnsafeActionErrors: 1

Trajectory evaluator
- ExactTrajectoryMatch: 0.5000
- ToolOrderAccuracy: 1.0000
- ArgumentSetF1Proxy: 0.9375
- TaskSuccessAgreement: 0.5000
- UnsafeToolSteps: 1

Policy checks
- High-risk RAG policy violations: 0
```

The contrast between `ToolSelectionAccuracy = 1.0` and `UnsafeActionErrors = 1`
is deliberate: selecting the right tool is not enough if the arguments are unsafe.

## QLoRA plan

The QLoRA configuration is included as a reproducible plan for future domain adaptation experiments.
The key point is not the specific loss curve, but the evaluation gates:

- citation support;
- refusal accuracy;
- tool-call argument accuracy;
- high-risk wrong-action rate.

## What this project proves

This is a small project, but it proves three practical skills:

1. how to define failure modes;
2. how to write evaluators that separate system components;
3. how to design guardrails before claiming an LLM application is production-ready.

