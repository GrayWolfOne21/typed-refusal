"""Fail-closed typed refusal contract.

A gate accepts a payload only when every required field is present and
sourced. Otherwise it emits NOT_READY or DATA_NULL and does not fill the gap.
"""

from typed_refusal.contract import (
    ACCEPT,
    DATA_NULL,
    NOT_READY,
    Contract,
    Decision,
    FieldRule,
)
from typed_refusal.gate import evaluate

__all__ = [
    "ACCEPT",
    "DATA_NULL",
    "NOT_READY",
    "Contract",
    "Decision",
    "FieldRule",
    "evaluate",
]

__version__ = "0.1.0"
