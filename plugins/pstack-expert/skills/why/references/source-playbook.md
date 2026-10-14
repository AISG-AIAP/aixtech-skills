# Source playbooks

The why skill spawns one investigator per available evidence category, each reading a single source-specific playbook below.

| Category | Playbook | Source it documents |
|---|---|---|
| Source control history | [`code-archaeology.md`](./sources/code-archaeology.md) | git, `gh` |
| Issue / ticket tracker | [`github-issues.md`](./sources/github-issues.md) | GitHub Issues through `gh` |

Cross-cutting:

- [`incident-postmortem.md`](./sources/incident-postmortem.md). Add this if the target code looks defensive (null checks, retry, timeout, rate limit, feature flag, egress guard, OOM handler).
