# Public boundary

This repository publishes one mechanism: a fail-closed typed refusal gate.

In:

- A contract of required fields.
- A payload.
- Source records that name a field and carry a source id.

Out:

- ACCEPT, only when every required field is present and sourced.
- NOT_READY, when a required field is missing or unsourced.
- DATA_NULL, when a required field is present but null, blank, or a placeholder.
- A SHA-256 seal of the decision.

Not in this repository:

- Domain rules, lexicons, classification tables, carrier logic, client files, or product names from any private system.
- A model, a prompt, or a policy that decides what a field means.
- Any path that fills a missing value.

The gate does not fetch evidence. It only checks that a caller already attached a source id. Empty evidence is not evidence.
