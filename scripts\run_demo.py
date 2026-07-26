"""Run the public deterministic-replay example."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from liquidityengine_research import EvidenceItem, MarketSnapshot, ReplayEngine


def main() -> None:
    fixture_path = ROOT / "examples" / "sample_market_state.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    snapshot = MarketSnapshot.from_dict(payload["snapshot"])
    evidence = tuple(EvidenceItem.from_dict(item) for item in payload["evidence"])
    record = ReplayEngine().replay(snapshot, evidence)

    print("LiquidityEngine Research - deterministic replay")
    print(json.dumps(record.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
