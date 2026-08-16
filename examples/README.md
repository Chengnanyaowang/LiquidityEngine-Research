# Synthetic examples

Every file in this directory is synthetic. The fixtures demonstrate public data contracts, bounded agent orchestration, and deterministic replay. They are not derived from a live market, customer account, private replay, or production strategy output.

- `sample_market_state.json`: complete evidence with unresolved structure.
- `scenarios/resolved_observation.json`: complete evidence admitted for research observation.
- `scenarios/event_risk.json`: an event boundary forces a wait state.
- `scenarios/incomplete_evidence.json`: missing leverage evidence forces review.

The public gate rejects any snapshot where `is_synthetic` is not `true`.
