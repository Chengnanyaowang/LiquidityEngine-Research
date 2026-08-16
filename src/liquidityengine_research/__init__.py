"""Public primitives for auditable research workflows.

This package intentionally contains no live trading strategy or execution code.
"""

from .agent import (
    AgentRunRecord,
    EvidenceToolbox,
    ResearchAgent,
    ResearchInterpretation,
    ResearchInterpreter,
    SyntheticResearchInterpreter,
    ToolInvocation,
)
from .models import DecisionAction, DecisionRecord, EvidenceItem, MarketSnapshot
from .policy import PermissionGate
from .replay import ReplayEngine

__all__ = [
    "AgentRunRecord",
    "DecisionAction",
    "DecisionRecord",
    "EvidenceToolbox",
    "EvidenceItem",
    "MarketSnapshot",
    "PermissionGate",
    "ResearchAgent",
    "ResearchInterpretation",
    "ResearchInterpreter",
    "ReplayEngine",
    "SyntheticResearchInterpreter",
    "ToolInvocation",
]

__version__ = "0.2.0"
