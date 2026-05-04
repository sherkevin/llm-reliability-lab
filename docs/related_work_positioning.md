# Positioning Against Existing Evaluation Frameworks

This portfolio is not trying to replace full-featured evaluation frameworks.
It is a small, readable lab that shows how to think about reliability metrics.

## RAGAS-style metrics

RAGAS popularized RAG-specific metrics such as faithfulness, answer relevancy,
context precision, and context recall. The local RAG evaluator in this project
keeps the same decomposition mindset but uses explicit gold evidence IDs so the
logic can be inspected without an LLM judge.

## TruLens-style tracing

TruLens emphasizes tracing and feedback functions. This project borrows the same
idea of component-level diagnosis: retrieval, citation, answer claims, tool calls,
and policy checks are evaluated separately.

## DeepEval-style metric suites

DeepEval provides many metrics and test integrations. This lab deliberately keeps
metrics small and transparent, so every score can be explained in an interview.

## MCP benchmark-style tool evaluation

Recent MCP and tool-use benchmarks focus on tool discovery, tool selection,
parameterization, syntax, dependency order, and task completion. This project
implements a miniature version of that idea:

- tool selection accuracy;
- argument exact match;
- required argument accuracy;
- trajectory order accuracy;
- unsafe tool action detection.

## Guardrails and refusal evaluation

Guardrails and refusal benchmarks focus on whether a model should answer, refuse,
or escalate. This lab includes risk-level checks and high-risk action detection
to separate fluent answers from safe answers.

## Why keep this project small

For a public portfolio, a compact and inspectable evaluator is more valuable than
a large opaque framework. The goal is to demonstrate judgment:

1. define failure modes;
2. separate components;
3. write reproducible metrics;
4. identify unsafe behavior;
5. document what a score does and does not prove.

