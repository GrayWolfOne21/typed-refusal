"""Fail-closed evaluator.

Accept only when every required field is present and, if required, sourced.
Otherwise return NOT_READY or DATA_NULL. Never invent a value.
"""

from __future__ import annotations

import hashlib
import json
from typing import Mapping

from typed_refusal.contract import (
    ACCEPT,
    DATA_NULL,
    NOT_READY,
    Contract,
    Decision,
    Source,
    is_null_value,
)


def evaluate(
    contract: Contract,
    payload: Mapping[str, object] | None,
    sources: list[Source] | tuple[Source, ...] | None = None,
) -> Decision:
    """Evaluate one payload against one contract.

    Missing key -> NOT_READY.
    Present but null, blank, or placeholder -> DATA_NULL.
    Required source absent, blank, or unmatched -> NOT_READY.
    DATA_NULL wins over NOT_READY when both fire, because a null is a
    stronger statement than a missing source: the field was offered and is empty.
    """

    body = dict(payload or {})
    by_field = _index_sources(sources or ())
    not_ready: list[str] = []
    data_null: list[str] = []
    reasons: list[str] = []
    accepted: dict[str, object] = {}

    for rule in contract.fields:
        if rule.name not in body:
            not_ready.append(rule.name)
            reasons.append(f"{rule.name}: missing")
            continue

        value = body[rule.name]
        if not rule.allow_empty and is_null_value(value):
            data_null.append(rule.name)
            reasons.append(f"{rule.name}: null")
            continue

        if rule.sourced:
            source = by_field.get(rule.name)
            if source is None or not source.source_id.strip():
                not_ready.append(rule.name)
                reasons.append(f"{rule.name}: unsourced")
                continue

        accepted[rule.name] = value

    if data_null:
        status = DATA_NULL
    elif not_ready:
        status = NOT_READY
    else:
        status = ACCEPT

    if status != ACCEPT:
        accepted = {}

    return Decision(
        status=status,
        contract=contract.name,
        accepted=accepted,
        not_ready=tuple(not_ready),
        data_null=tuple(data_null),
        reasons=tuple(reasons),
    )


def seal(decision: Decision) -> str:
    """SHA-256 of the canonical decision. Refusal is a receipt, not a log line."""

    payload = {
        "status": decision.status,
        "contract": decision.contract,
        "accepted": decision.accepted,
        "not_ready": list(decision.not_ready),
        "data_null": list(decision.data_null),
        "reasons": list(decision.reasons),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _index_sources(sources: list[Source] | tuple[Source, ...]) -> dict[str, Source]:
    indexed: dict[str, Source] = {}
    for source in sources:
        # First sourced record wins. A later blank record cannot erase it.
        indexed.setdefault(source.field, source)
    return indexed
