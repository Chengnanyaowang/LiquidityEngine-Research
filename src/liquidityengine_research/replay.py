"""Deterministic replay for public, synthetic decision fixtures."""

from __future__ import annotations

from hashlib import sha256
from typing import Iterable

from .models import DecisionRecord, EvidenceItem, MarketSnapshot
from .policy import PermissionGate


class ReplayEngine:
    """Rebuilds the public decision record from fixed inputs without a model call."""

    schema_version = "decision-record.v1"

    def __init__(self, gate: PermissionGate | None = None) -> None:
        self._gate = gate or PermissionGate()

    def replay(
        self,
        snapshot: MarketSnapshot,
        evidence: Iterable[EvidenceItem],
    ) -> DecisionRecord:
        evidence = tuple(evidence)
        result = self._gate.evaluate(snapshot, evidence)
        evidence_ids = tuple(item.evidence_id for item in evidence)
        facts_digest = self._digest(snapshot, evidence)
        decision_id = sha256(
            f"{self.schema_version}|{snapshot.snapshot_id}|{facts_digest}".encode()
        ).hexdigest()[:16]

        return DecisionRecord(
            schema_version=self.schema_version,
            decision_id=decision_id,
            snapshot_id=snapshot.snapshot_id,
            action=result.action,
            permission_status=result.permission_status,
            reason_codes=result.reason_codes,
            evidence_ids=evidence_ids,
            facts_digest=facts_digest,
        )

    @staticmethod
    def _digest(
        snapshot: MarketSnapshot,
        evidence: tuple[EvidenceItem, ...],
    ) -> str:
        snapshot_payload = (
            snapshot.snapshot_id,
            snapshot.as_of_utc,
            snapshot.source,
            snapshot.is_synthetic,
            snapshot.price,
            snapshot.price_structure,
            snapshot.open_interest_change_pct,
            snapshot.liquidation_context,
            snapshot.event_risk,
        )
        evidence_payload = tuple(
            (item.evidence_id, item.category, item.summary, item.provenance, item.value)
            for item in evidence
        )
        return sha256(repr((snapshot_payload, evidence_payload)).encode()).hexdigest()
