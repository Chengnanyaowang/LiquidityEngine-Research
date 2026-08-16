"""A bounded, synthetic research-agent orchestration example.

The module demonstrates tool use, structured interpretation, deterministic
authorization, and an auditable run record. It contains no live model call,
market strategy, or execution path.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Protocol

from .models import DecisionAction, DecisionRecord, EvidenceItem, MarketSnapshot
from .policy import PermissionGate
from .replay import ReplayEngine


@dataclass(frozen=True)
class ToolInvocation:
    """One deterministic inspection performed before interpretation."""

    name: str
    input_ref: str
    output: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResearchInterpretation:
    """A non-executable, structured interpretation of synthetic evidence."""

    interpretation_id: str
    provider: str
    summary: str
    requested_action: DecisionAction
    uncertainty: tuple[str, ...]
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["requested_action"] = self.requested_action.value
        payload["uncertainty"] = list(self.uncertainty)
        payload["evidence_ids"] = list(self.evidence_ids)
        return payload


@dataclass(frozen=True)
class AgentRunRecord:
    """The complete public trace for one bounded research-agent run."""

    schema_version: str
    run_id: str
    snapshot_id: str
    tool_invocations: tuple[ToolInvocation, ...]
    interpretation: ResearchInterpretation
    decision: DecisionRecord

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "snapshot_id": self.snapshot_id,
            "tool_invocations": [item.to_dict() for item in self.tool_invocations],
            "interpretation": self.interpretation.to_dict(),
            "decision": self.decision.to_dict(),
            "disclosure": "Synthetic research state only; not a trading instruction.",
        }


class ResearchInterpreter(Protocol):
    """Interface implemented by an interpretation provider."""

    provider_name: str

    def interpret(
        self,
        snapshot: MarketSnapshot,
        evidence: tuple[EvidenceItem, ...],
        tool_invocations: tuple[ToolInvocation, ...],
    ) -> ResearchInterpretation:
        """Return a structured research interpretation."""


class EvidenceToolbox:
    """Deterministic tools exposed to the public synthetic agent."""

    def __init__(self, required_categories: frozenset[str] | None = None) -> None:
        self.required_categories = required_categories or PermissionGate.required_categories

    def inspect(
        self,
        snapshot: MarketSnapshot,
        evidence: tuple[EvidenceItem, ...],
    ) -> tuple[ToolInvocation, ...]:
        categories = sorted({item.category for item in evidence})
        missing = sorted(self.required_categories - set(categories))
        return (
            ToolInvocation(
                name="inspect_evidence_categories",
                input_ref=snapshot.snapshot_id,
                output={"present": categories, "missing": missing},
            ),
            ToolInvocation(
                name="inspect_event_boundary",
                input_ref=snapshot.snapshot_id,
                output={"event_risk": snapshot.event_risk},
            ),
            ToolInvocation(
                name="inspect_structure_state",
                input_ref=snapshot.snapshot_id,
                output={"price_structure": snapshot.price_structure},
            ),
        )


class SyntheticResearchInterpreter:
    """Offline interpreter used to keep the public demo reproducible and safe."""

    provider_name = "synthetic_offline_interpreter"

    def interpret(
        self,
        snapshot: MarketSnapshot,
        evidence: tuple[EvidenceItem, ...],
        tool_invocations: tuple[ToolInvocation, ...],
    ) -> ResearchInterpretation:
        categories = {item.category for item in evidence}
        missing = sorted(PermissionGate.required_categories - categories)

        if missing:
            summary = "The synthetic evidence bundle is incomplete and needs review."
            requested_action = DecisionAction.REVIEW
            uncertainty = tuple(f"missing_{item}" for item in missing)
        elif snapshot.event_risk != "normal":
            summary = "A synthetic event boundary is active; defer interpretation."
            requested_action = DecisionAction.WAIT
            uncertainty = ("event_window_active",)
        elif snapshot.price_structure == "unresolved":
            summary = "Synthetic structure evidence is present but remains unresolved."
            requested_action = DecisionAction.WAIT
            uncertainty = ("structure_unresolved",)
        else:
            summary = "Synthetic evidence is complete for bounded research observation."
            requested_action = DecisionAction.OBSERVE
            uncertainty = ()

        evidence_ids = tuple(item.evidence_id for item in evidence)
        identity_payload = json.dumps(
            {
                "snapshot_id": snapshot.snapshot_id,
                "evidence_ids": evidence_ids,
                "requested_action": requested_action.value,
                "uncertainty": uncertainty,
                "tools": [item.name for item in tool_invocations],
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        interpretation_id = sha256(identity_payload.encode()).hexdigest()[:16]
        return ResearchInterpretation(
            interpretation_id=interpretation_id,
            provider=self.provider_name,
            summary=summary,
            requested_action=requested_action,
            uncertainty=uncertainty,
            evidence_ids=evidence_ids,
        )


class ResearchAgent:
    """Orchestrates evidence tools and interpretation without granting authority."""

    schema_version = "agent-run.v1"

    def __init__(
        self,
        interpreter: ResearchInterpreter | None = None,
        toolbox: EvidenceToolbox | None = None,
        replay: ReplayEngine | None = None,
    ) -> None:
        self._interpreter = interpreter or SyntheticResearchInterpreter()
        self._toolbox = toolbox or EvidenceToolbox()
        self._replay = replay or ReplayEngine()

    def run(
        self,
        snapshot: MarketSnapshot,
        evidence: tuple[EvidenceItem, ...],
    ) -> AgentRunRecord:
        evidence = tuple(evidence)
        tool_invocations = self._toolbox.inspect(snapshot, evidence)
        interpretation = self._interpreter.interpret(
            snapshot,
            evidence,
            tool_invocations,
        )
        decision = self._replay.replay(snapshot, evidence)
        run_payload = "|".join(
            (
                self.schema_version,
                snapshot.snapshot_id,
                interpretation.interpretation_id,
                decision.decision_id,
            )
        )
        run_id = sha256(run_payload.encode()).hexdigest()[:16]
        return AgentRunRecord(
            schema_version=self.schema_version,
            run_id=run_id,
            snapshot_id=snapshot.snapshot_id,
            tool_invocations=tool_invocations,
            interpretation=interpretation,
            decision=decision,
        )
