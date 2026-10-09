# Changelog

## Unreleased

Documented on `main` after the immutable `v0.1.0` tag. The tag still points at `712f2b5` and does not include these notes.

- README run commands now set `PYTHONPATH=src`, or use `pip install -e .`. A fresh clone of `v0.1.0` failed with `No module named typed_refusal` because the package lives under `src/`.
- README states the status split in the code: a missing key is `NOT_READY`; a present null, blank, or placeholder is `DATA_NULL`.
- `Decision` keeps the source chain. `seal()` hashes each source field, source id, locator, and digest. A moved locator or a changed digest changes the seal.

### Credit

Marius Andronie, Devaland Marketing S.R.L., reported both findings on 8 October 2026 while running `v0.1.0` against a synthetic deal script:

- The fresh-clone install failure, and that `PYTHONPATH=src` makes the seven tests pass.
- The seal did not bind a source locator. A locator moved to another page left the seal unchanged. A forensic hash that omits the document digest and the locator array does not lock the citation.

The locator and digest binding on `main` closes that gap in this repository. `v0.1.0` does not include it.

## 0.1.0

Fail-closed gate. Accepts a payload only when every required field is present and sourced. Otherwise returns `NOT_READY` or `DATA_NULL` and does not fill the gap. Commit `712f2b5`. Release is immutable.
