import json
from pathlib import Path

from liquidityengine_research import (
    DecisionAction,
    EvidenceItem,
    MarketSnapshot,
    ResearchAgent,
    ResearchInterpretation,
)


ROOT = Path(__file__).resolve().parents[1]


def _snapshot(**overrides):
    payload = {
        "snapshot_id": "synthetic-agent-001",
        "as_of_utc": "2026-07-01T12:00:00Z",
        "source": "synthetic_fixture",
        "is_synthetic": True,
        "price": 60000.0,
        "price_structure": "resolved",
        "open_interest_change_pct": 0.2,
        "liquidation_context": "normal_activity",
        "event_risk": "normal",
    }
    payload.update(overrides)
    return MarketSnapshot.from_dict(payload)


def _evidence(*categories):
    return tuple(
        EvidenceItem(
            evidence_id=f"agent-evidence-{index}",
            category=category,
            summary="Synthetic agent test fact.",
            provenance="synthetic_test",
        )
        for index, category in enumerate(categories, start=1)
    )


def _complete_evidence():
    return _evidence("market_structure", "leverage_context", "event_context")


def _load_scenario(name):
    path = ROOT / "examples" / "scenarios" / name
    payload = json.loads(path.read_text(encoding="utf-8"))
    snapshot = MarketSnapshot.from_dict(payload["snapshot"])
    evidence = tuple(EvidenceItem.from_dict(item) for item in payload["evidence"])
    return snapshot, evidence


def test_agent_records_deterministic_tool_invocations():
    record = ResearchAgent().run(_snapshot(), _complete_evidence())

    assert [item.name for item in record.tool_invocations] == [
        "inspect_evidence_categories",
        "inspect_event_boundary",
        "inspect_structure_state",
    ]
    assert record.tool_invocations[0].output["missing"] == []


def test_agent_run_is_deterministic_for_fixed_synthetic_facts():
    agent = ResearchAgent()
    first = agent.run(_snapshot(), _complete_evidence())
    second = agent.run(_snapshot(), _complete_evidence())

    assert first.to_dict() == second.to_dict()
    assert first.run_id == second.run_id


def test_agent_keeps_local_gate_as_final_authority():
    class PermissiveInterpreter:
        provider_name = "permissive_test_interpreter"

        def interpret(self, snapshot, evidence, tool_invocations):
            return ResearchInterpretation(
                interpretation_id="permissive-test",
                provider=self.provider_name,
                summary="Synthetic test requests observation.",
                requested_action=DecisionAction.OBSERVE,
                uncertainty=(),
                evidence_ids=tuple(item.evidence_id for item in evidence),
            )

    record = ResearchAgent(interpreter=PermissiveInterpreter()).run(
        _snapshot(event_risk="scheduled_release"),
        _complete_evidence(),
    )

    assert record.interpretation.requested_action is DecisionAction.OBSERVE
    assert record.decision.action is DecisionAction.WAIT
    assert record.decision.reason_codes == ("event_context_requires_review",)


def test_resolved_scenario_is_admitted_for_observation_only():
    snapshot, evidence = _load_scenario("resolved_observation.json")
    record = ResearchAgent().run(snapshot, evidence)

    assert record.decision.action is DecisionAction.OBSERVE
    assert record.decision.permission_status == "admitted_for_research"


def test_event_risk_scenario_is_deferred():
    snapshot, evidence = _load_scenario("event_risk.json")
    record = ResearchAgent().run(snapshot, evidence)

    assert record.interpretation.requested_action is DecisionAction.WAIT
    assert record.decision.action is DecisionAction.WAIT


def test_incomplete_scenario_requires_review():
    snapshot, evidence = _load_scenario("incomplete_evidence.json")
    record = ResearchAgent().run(snapshot, evidence)

    assert record.interpretation.requested_action is DecisionAction.REVIEW
    assert record.decision.action is DecisionAction.REVIEW
    assert "missing_leverage_context" in record.decision.reason_codes


def test_agent_record_contains_no_execution_instruction_fields():
    payload = ResearchAgent().run(_snapshot(), _complete_evidence()).to_dict()
    serialized = json.dumps(payload).lower()

    assert '"entry"' not in serialized
    assert '"position_size"' not in serialized
    assert '"stop_loss"' not in serialized
    assert payload["disclosure"].startswith("Synthetic research state")


def test_non_synthetic_snapshot_is_blocked_by_public_gate():
    record = ResearchAgent().run(
        _snapshot(is_synthetic=False),
        _complete_evidence(),
    )

    assert record.decision.action is DecisionAction.REVIEW
    assert record.decision.reason_codes == ("public_demo_requires_synthetic_data",)
