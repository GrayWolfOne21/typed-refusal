# typed-refusal

Fail-closed typed refusal contract.

A gate accepts a payload only when every required field is present and sourced. Otherwise it emits `NOT_READY` or `DATA_NULL` and does not fill the gap.

```python
from typed_refusal import Contract, FieldRule, evaluate
from typed_refusal.contract import Source

contract = Contract(
    name="payout",
    fields=(FieldRule("payee"), FieldRule("amount")),
)

decision = evaluate(
    contract,
    {"payee": "acme"},
    [Source("payee", "vendor-file")],
)

decision.status      # NOT_READY
decision.not_ready   # ("amount",)
decision.accepted    # {}
```

`amount` is not invented. The refusal names the missing field.

## Status

| Status | When |
| --- | --- |
| `ACCEPT` | Every required field is present, non-null, and sourced when the rule requires a source. |
| `NOT_READY` | A required field is missing, or present but has no source id. |
| `DATA_NULL` | A required field is present but null, blank, empty, or a placeholder (`N/A`, `unknown`, `tbd`). |

`DATA_NULL` wins when both fire. A null is a stronger statement than a missing source.

A missing key is `NOT_READY`. A present null, blank, or placeholder is `DATA_NULL`. Those are not interchangeable.

## Seal

`seal()` hashes the decision: status, contract name, accepted values, the two refusal lists, and reasons. It does not hash a document digest or a page locator. Moving a locator to another page does not change the seal. That gap was reported by Marius Andronie. It is not closed in this tree. See [CHANGELOG.md](CHANGELOG.md).

## What this is not

This is a reference implementation of a gate, not a claim that fail-closed refusal is new. Related public work already treats stop as a first-class result and returns the missing set on reject.

No domain rules ship here. See [PUBLIC_BOUNDARY.md](PUBLIC_BOUNDARY.md).

## Run

The package lives under `src/`. A fresh clone needs that path, or an editable install.

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python examples/minimal.py
```

Or:

```bash
pip install -e .
python -m unittest discover -s tests
python examples/minimal.py
```

Requires Python 3.10+. No third-party dependencies to run the tests. `pip install -e .` needs setuptools.

## License

MIT. See [LICENSE](LICENSE).
