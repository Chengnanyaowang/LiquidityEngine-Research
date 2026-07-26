"""Stable, public data contracts for a research decision record."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class DecisionAction(str, Enum):
    """Research-only actions; none represents a trading instruction."""

    OBSERVE = "observe"
    WAIT = "wait"
    REVIEW = "review"


@dataclass(frozen=True)
class MarketSnapshot:
    """A normalized, synthetic market-state observation."""

    snapshot_id: str
    as_of_utc: str
    source: str
    is_synthetic: bool
    price: float
    price_structure: str
    open_interest_change_pct: float
    liquidation_context: str
    event_risk: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MarketSnapshot":
        return cls(**payload)


@dataclass(frozen=True)
class EvidenceItem:
    """One attributable fact that contributed to a research decision."""

    evidence_id: str
    category: str
    summary: str
    provenance: str
    value: str | float | int | bool | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EvidenceItem":
        return cls(**payload)


@dataclass(frozen=True)
class DecisionRecord:
    """An immutable record suitable for deterministic replay and review."""

    schema_version: str
    decision_id: str
    snapshot_id: str
    action: DecisionAction
    permission_status: str
    reason_codes: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    facts_digest: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["action"] = self.action.value
        payload["reason_codes"] = list(self.reason_codes)
        payload["evidence_ids"] = list(self.evidence_ids)
        return payload
