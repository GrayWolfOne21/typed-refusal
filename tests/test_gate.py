"""Tests for the fail-closed typed refusal gate."""

import unittest

from typed_refusal import ACCEPT, DATA_NULL, NOT_READY, Contract, FieldRule, evaluate
from typed_refusal.contract import Source
from typed_refusal.gate import seal


CLAIM = Contract(
    name="claim",
    fields=(
        FieldRule("subject"),
        FieldRule("amount"),
        FieldRule("note", sourced=False),
    ),
)


class GateTests(unittest.TestCase):
    def test_accepts_only_when_required_fields_are_present_and_sourced(self):
        decision = evaluate(
            CLAIM,
            {"subject": "invoice-9", "amount": 40, "note": "ok"},
            [
                Source("subject", "doc-1", "file://invoice-9"),
                Source("amount", "doc-1", "file://invoice-9", digest="abc"),
            ],
        )
        self.assertEqual(decision.status, ACCEPT)
        self.assertTrue(decision.ok)
        self.assertEqual(decision.accepted["amount"], 40)
        self.assertEqual(decision.not_ready, ())
        self.assertEqual(decision.data_null, ())

    def test_missing_field_is_not_ready_and_is_not_filled(self):
        decision = evaluate(
            CLAIM,
            {"subject": "invoice-9"},
            [Source("subject", "doc-1")],
        )
        self.assertEqual(decision.status, NOT_READY)
        self.assertIn("amount", decision.not_ready)
        self.assertIn("note", decision.not_ready)
        self.assertEqual(decision.accepted, {})
        self.assertNotIn("amount", decision.accepted)

    def test_null_placeholder_is_data_null(self):
        decision = evaluate(
            CLAIM,
            {"subject": "invoice-9", "amount": "N/A", "note": ""},
            [Source("subject", "doc-1"), Source("amount", "doc-1")],
        )
        self.assertEqual(decision.status, DATA_NULL)
        self.assertEqual(decision.data_null, ("amount", "note"))

    def test_present_but_unsourced_is_not_ready(self):
        decision = evaluate(
            CLAIM,
            {"subject": "invoice-9", "amount": 40, "note": "ok"},
            [Source("subject", "doc-1")],
        )
        self.assertEqual(decision.status, NOT_READY)
        self.assertEqual(decision.not_ready, ("amount",))
        self.assertIn("amount: unsourced", decision.reasons)

    def test_blank_source_id_does_not_count(self):
        decision = evaluate(
            CLAIM,
            {"subject": "invoice-9", "amount": 40, "note": "ok"},
            [Source("subject", "doc-1"), Source("amount", "   ")],
        )
        self.assertEqual(decision.status, NOT_READY)
        self.assertIn("amount", decision.not_ready)

    def test_none_payload_refuses_every_field(self):
        decision = evaluate(CLAIM, None, None)
        self.assertEqual(decision.status, NOT_READY)
        self.assertEqual(decision.not_ready, ("subject", "amount", "note"))

    def test_seal_is_stable(self):
        decision = evaluate(CLAIM, {"subject": "x"}, [])
        self.assertEqual(seal(decision), seal(decision))
        self.assertEqual(len(seal(decision)), 64)


if __name__ == "__main__":
    unittest.main()
