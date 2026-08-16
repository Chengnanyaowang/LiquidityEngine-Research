# Evaluation methodology

The product objective is not to make an AI sound decisive. It is to evaluate whether a research workflow remains evidence-grounded, bounded, and reproducible.

## Public checks

This repository tests the properties that can be demonstrated without revealing private research IP:

1. The same synthetic input yields the same decision record and digest.
2. Missing evidence produces an explicit block rather than an implied decision.
3. An event-risk state produces a review or wait state.
4. The public reference rejects non-synthetic input.
5. A permissive interpreter cannot override the deterministic permission gate.
6. An agent run records every public tool invocation and contains no execution fields.

## Private evaluation

The production team separately evaluates data quality, decision consistency, historical replay fidelity, and research alignment against access-controlled fixtures. Those artifacts may be made available in a controlled diligence process, but are intentionally not published in this repository.

## What we do not claim

This project does not claim a public trading-performance metric, a guaranteed return, or a benchmark that predicts future market outcomes. Research quality, auditability, and product reliability are separate from investment performance.
