# Decision record contract

A decision record is a compact, immutable research artifact. It does not contain an execution instruction or private strategy rationale.

```json
{
  "schema_version": "decision-record.v1",
  "decision_id": "2b991fe2c3d0a2fd",
  "snapshot_id": "synthetic-btc-001",
  "action": "wait",
  "permission_status": "deferred",
  "reason_codes": ["structure_not_resolved"],
  "evidence_ids": ["structure-001", "leverage-001", "event-001"],
  "facts_digest": "sha256..."
}
```

## Contract guarantees

- **Traceability:** a record points to the snapshot and evidence IDs used to create it.
- **Reproducibility:** the fact digest is derived from a stable serialization of those inputs.
- **Separation:** `action` represents a research workflow state, never a buy/sell instruction.
- **Reviewability:** `reason_codes` are machine-readable and human-explainable.

## What is excluded

Private model prompts, proprietary strategy labels, confidence thresholds, pricing of data sources, customer identities, and execution instructions do not belong in the public contract.
