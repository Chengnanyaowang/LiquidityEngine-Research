"""A deliberately conservative public permission gate.

The gate demonstrates engineering separation between interpretation and
authorization. It is not a market strategy and cannot emit an entry signal.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import DecisionAction, EvidenceItem, MarketSnapshot


@dataclass(frozen=True)
class PermissionResult:
    action: DecisionAction
    permission_status: str
    reason_codes: tuple[str, ...]


class PermissionGate:
    """Checks evidence completeness and high-level risk boundaries.

    The public reference intentionally keeps the policy generic. Production
    systems can implement their own private research methods behind the same
    decision-record contract.
    """

    required_categories = frozenset(
        {"market_structure", "leverage_context", "event_context"}
    )

    def evaluate(
        self,
        snapshot: MarketSnapshot,
        evidence: Iterable[EvidenceItem],
    ) -> PermissionResult:
        evidence = tuple(evidence)
        categories = {item.category for item in evidence}
        missing = sorted(self.required_categories - categories)

        if not snapshot.is_synthetic:
            return PermissionResult(
                action=DecisionAction.REVIEW,
                permission_status="blocked",
                reason_codes=("public_demo_requires_synthetic_data",),
            )

        if snapshot.event_risk != "normal":
            return PermissionResult(
                action=DecisionAction.WAIT,
                permission_status="deferred",
                reason_codes=("event_context_requires_review",),
            )

        if missing:
            return PermissionResult(
                action=DecisionAction.REVIEW,
                permission_status="blocked",
                reason_codes=tuple(f"missing_{category}" for category in missing),
            )

        if snapshot.price_structure == "unresolved":
            return PermissionResult(
                action=DecisionAction.WAIT,
                permission_status="deferred",
                reason_codes=("structure_not_resolved",),
            )

        return PermissionResult(
            action=DecisionAction.OBSERVE,
            permission_status="admitted_for_research",
            reason_codes=("evidence_bundle_complete",),
        )
