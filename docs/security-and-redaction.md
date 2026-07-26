# Security and redaction policy

## Public-material rule

Every committed file must be safe for permanent public distribution. The following are never accepted into this repository:

- API keys, tokens, exchange cookies, account IDs, or private endpoints.
- Raw production `runtime/`, `records/`, replay checkpoints, or alert history.
- Proprietary strategy theory, rule thresholds, prompts, model-routing settings, or feature weights.
- Customer names, design-partner identifiers, trading positions, PnL, or confidential discussions.

## Synthetic-first examples

Public fixtures use `source="synthetic_fixture"` and `is_synthetic=true`. The example gate rejects a non-synthetic snapshot. This is both a code-level guard and a contributor signal: a polished demo must not quietly become a data leak.

## Media policy

Public screenshots or video should show only approved product surfaces. Before release, review visible browser tabs, local paths, API credentials, private labels, and personally identifying information. Use a hosted demo link or a compressed poster image rather than committing large raw recordings.

## Incident response

If a secret is committed, revoke or rotate it immediately. Removing it from the latest branch is insufficient because Git history may still expose it. Follow the reporting process in [SECURITY.md](../SECURITY.md).
