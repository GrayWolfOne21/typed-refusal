"""Contract types. No domain rules live here."""

from __future__ import annotations

from dataclasses import dataclass


ACCEPT = "ACCEPT"
NOT_READY = "NOT_READY"
DATA_NULL = "DATA_NULL"

# Values that look filled but carry no evidence. The gate treats these as null.
_NULL_TOKENS = frozenset({"", "null", "none", "n/a", "na", "unknown", "tbd", "-"})


@dataclass(frozen=True)
class FieldRule:
    """One required field.

    present: the key must exist on the payload.
    sourced: a source record must name this field and carry a non-empty source id.
    allow_empty: opt out of the null-token check. Default is fail-closed.
    """

    name: str
    sourced: bool = True
    allow_empty: bool = False


@dataclass(frozen=True)
class Contract:
    """The required set. The gate never adds fields and never supplies defaults."""

    name: str
    fields: tuple[FieldRule, ...]

    def __post_init__(self) -> None:
        names = [field.name for field in self.fields]
        if len(names) != len(set(names)):
            raise ValueError("contract field names must be unique")
        if not names:
            raise ValueError("contract must require at least one field")


@dataclass(frozen=True)
class Source:
    """A provenance record. The gate does not fetch the artifact."""

    field: str
    source_id: str
    locator: str = ""
    digest: str = ""


@dataclass(frozen=True)
class Decision:
    """A typed result. Refusal lists exactly what is missing or null."""

    status: str
    contract: str
    accepted: dict
    not_ready: tuple[str, ...]
    data_null: tuple[str, ...]
    reasons: tuple[str, ...]
    sources: tuple[Source, ...] = ()

    @property
    def ok(self) -> bool:
        return self.status == ACCEPT


def is_null_value(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in _NULL_TOKENS:
        return True
    if isinstance(value, (list, dict)) and len(value) == 0:
        return True
    return False
