# Datawhale GOAI - AI + Finance submission overview

## Project statement

LiquidityEngine Research demonstrates a bounded AI research agent for crypto-derivatives workflows. It converts synthetic market observations into attributable evidence, tool traces, structured interpretations, deterministic permission decisions, and replayable records.

The competition demonstration focuses on research quality and risk governance. It does not provide deterministic investment advice or execute transactions.

## Agent workflow

1. Load a synthetic market snapshot and attributable evidence items.
2. Use bounded tools to inspect evidence completeness, event boundaries, and structure state.
3. Produce a structured, non-executable interpretation.
4. Apply an independent deterministic permission gate.
5. Store an agent run and decision record for replay and review.

Run all public scenarios:

```bash
python scripts/run_agent_demo.py --scenario all
```

## Why this is an Agent rather than a single prompt

- It operates over typed state and evidence rather than an unstructured chat message.
- It calls explicit tools and records their outputs.
- Interpretation and authorization are separate components.
- A permissive interpretation cannot override event or evidence controls.
- Every run produces a stable trace that can be evaluated after the fact.

## Public safety boundary

The repository contains only synthetic fixtures and an offline interpreter. Private strategy definitions, production prompts, live data connectors, credentials, user records, and execution capabilities are excluded.

## Team roles

- Zhang Qingyu: product, engineering, data workflow, reliability, and presentation.
- Li Runpeng: market research, strategy semantics, scenario review, and domain evaluation.
- Faculty advisor: project guidance, material review, and responsible-use communication for the competition submission.

## Evaluation targets

- deterministic replay for fixed evidence;
- explicit failure on missing evidence;
- event-risk deferral;
- local authorization remaining authoritative;
- no execution fields in public agent records.
