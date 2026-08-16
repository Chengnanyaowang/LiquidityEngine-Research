"""Run the bounded synthetic research-agent scenarios."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from liquidityengine_research import EvidenceItem, MarketSnapshot, ResearchAgent


SCENARIOS = {
    "unresolved": ROOT / "examples" / "sample_market_state.json",
    "resolved": ROOT / "examples" / "scenarios" / "resolved_observation.json",
    "event-risk": ROOT / "examples" / "scenarios" / "event_risk.json",
    "incomplete": ROOT / "examples" / "scenarios" / "incomplete_evidence.json",
}


def run_scenario(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    snapshot = MarketSnapshot.from_dict(payload["snapshot"])
    evidence = tuple(EvidenceItem.from_dict(item) for item in payload["evidence"])
    return ResearchAgent().run(snapshot, evidence).to_dict()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        choices=("all", *SCENARIOS),
        default="all",
        help="Synthetic scenario to run.",
    )
    parser.add_argument("--json", action="store_true", help="Print complete JSON traces.")
    args = parser.parse_args()

    names = SCENARIOS if args.scenario == "all" else (args.scenario,)
    print("LiquidityEngine Research - bounded synthetic agent")
    for name in names:
        record = run_scenario(SCENARIOS[name])
        if args.json:
            print(json.dumps({"scenario": name, "record": record}, indent=2))
            continue
        decision = record["decision"]
        print(
            f"{name:12} action={decision['action']:7} "
            f"permission={decision['permission_status']:23} "
            f"tools={len(record['tool_invocations'])}"
        )


if __name__ == "__main__":
    main()
