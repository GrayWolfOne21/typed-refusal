"""Minimal caller. The gate does not fill a missing amount."""

from typed_refusal import Contract, FieldRule, evaluate
from typed_refusal.contract import Source
from typed_refusal.gate import seal

contract = Contract(
    name="payout",
    fields=(FieldRule("payee"), FieldRule("amount"), FieldRule("memo", sourced=False)),
)

decision = evaluate(
    contract,
    {"payee": "acme", "amount": None, "memo": ""},
    [Source("payee", "vendor-file", "file://vendors/acme")],
)

print(decision.status)
print(decision.reasons)
print(seal(decision))
