"""
Monitoring and Safety package for CareerPilot.

This package contains:
- Safety rules and forbidden topics
- Mechanical risk and hallucination checks
- Safety logging utilities
"""

from .safety_rules import FORBIDDEN_TOPICS, SAFETY_MESSAGES
from .risk_checks import check_hallucination, check_forbidden_content, validate_rag_reliability
from .logs import log_safety_event

__all__ = [
    "FORBIDDEN_TOPICS", 
    "SAFETY_MESSAGES", 
    "check_hallucination", 
    "check_forbidden_content",
    "validate_rag_reliability",
    "log_safety_event"
]