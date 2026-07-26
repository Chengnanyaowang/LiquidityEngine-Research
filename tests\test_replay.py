from liquidityengine_research import EvidenceItem, MarketSnapshot, ReplayEngine


def _snapshot(**overrides):
    payload = {
        "snapshot_id": "fixture-001",
        "as_of_utc": "2026-07-01T12:00:00Z",
        "source": "synthetic_fixture",
        "is_synthetic": True,
        "price": 60000.0,
        "price_structure": "unresolved",
        "open_interest_change_pct": 0.8,
        "liquidation_context": "concentrated_activity",
        "event_risk": "normal",
    }
    payload.update(overrides)
    return MarketSnapshot.from_dict(payload)


def _evidence(*categories):
    return tuple(
        EvidenceItem(
            evidence_id=f"evidence-{index}",
            category=category,
            summary="Synthetic test fact.",
            provenance="synthetic_test",
        )
        for index, category in enumerate(categories, start=1)
    )


def test_replay_is_deterministic_for_fixed_facts():
    engine = ReplayEngine()
    snapshot = _snapshot()
    evidence = _evidence("market_structure", "leverage_context", "event_context")

    first = engine.replay(snapshot, evidence)
    second = engine.replay(snapshot, evidence)

    assert first.to_dict() == second.to_dict()
    assert first.action.value == "wait"
    assert first.reason_codes == ("structure_not_resolved",)


def test_gate_blocks_incomplete_evidence_bundle():
    record = ReplayEngine().replay(
        _snapshot(price_structure="resolved"),
        _evidence("market_structure", "event_context"),
    )

    assert record.action.value == "review"
    assert record.permission_status == "blocked"
    assert record.reason_codes == ("missing_leverage_context",)


def test_gate_defers_event_risk_without_generating_trade_instruction():
    record = ReplayEngine().replay(
        _snapshot(price_structure="resolved", event_risk="scheduled_release"),
        _evidence("market_structure", "leverage_context", "event_context"),
    )

    assert record.action.value == "wait"
    assert record.permission_status == "deferred"
    assert "entry" not in record.to_dict()


def test_public_reference_rejects_non_synthetic_input():
    record = ReplayEngine().replay(
        _snapshot(is_synthetic=False, price_structure="resolved"),
        _evidence("market_structure", "leverage_context", "event_context"),
    )

    assert record.action.value == "review"
    assert record.reason_codes == ("public_demo_requires_synthetic_data",)
