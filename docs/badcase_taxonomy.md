# Badcase Taxonomy

This taxonomy separates failures by the component that should be fixed.

## 1. Retrieval failure

The answer is wrong because the correct evidence was not retrieved.

Signals:

- low Recall@K;
- gold chunk not in top-K;
- query rewrite missing exact fault codes or component names.

Fixes:

- hybrid BM25 + dense retrieval;
- better chunking;
- metadata filters;
- reranker training.

## 2. Evidence-use failure

The correct evidence is in context, but the answer ignores or misreads it.

Signals:

- gold chunk retrieved;
- citation exists;
- claim not supported by cited text.

Fixes:

- citation-aware prompting;
- SFT on evidence-grounded answers;
- claim-level verifier.

## 3. Unsupported citation

The answer cites a chunk, but the chunk does not support the claim.

Signals:

- high retrieval hit rate;
- low citation precision;
- unsupported key claims.

Fixes:

- citation verifier;
- claim decomposition;
- answer regeneration with evidence constraints.

## 4. Refusal failure

The model answers when it should refuse or escalate.

Signals:

- retrieval empty or contradictory;
- high-risk operation;
- confident answer without evidence.

Fixes:

- refusal data;
- DPO pairs where safe refusal beats fluent hallucination;
- risk-level policy gate.

## 5. Unsafe tool action

The agent selects a tool or arguments that may trigger unsafe actions.

Signals:

- high-risk operation with `allow_direct_action=true`;
- missing citation requirement;
- invalid permission scope.

Fixes:

- schema constraints;
- argument validation;
- human confirmation for high-risk tools.

