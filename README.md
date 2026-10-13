# aixtech-skills

Agent skills for aixtech, at <https://github.com/AISG-AIAP/aixtech-skills>. The repo is a plugin marketplace for Claude Code and Codex. Each plugin's `skills/` directory also works in any harness that reads Agent Skills.

| Plugin | Contents |
|---|---|
| `pstack-starter` | `/pstack` with the Feature, Babysit, and Shipping playbooks, the `how`, `architect`, `arena`, and `interrogate` skills Feature uses, and the 17 principles they need. The first level of the course. |

## pstack-starter

`pstack-starter` is a harness-agnostic port of part of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, taken from upstream commit `1dcc2ba`.

- `plugins/pstack-starter/skills/pstack` is the single entry point, upstream's `/poteto-mode` renamed and trimmed to this level. It routes each task to a playbook in `skills/pstack/playbooks/` and grounds every decision in the principles.
- `plugins/pstack-starter/skills/how`, `architect`, `arena`, and `interrogate` are the skills the Feature playbook uses.
- `plugins/pstack-starter/skills/principle-*` holds the 17 principles those skills and playbooks cite.

Invoke it with `/pstack` in Claude Code (`/pstack-starter:pstack` also works). Codex prefixes plugin skills with the plugin name, so there it is `$pstack-starter:pstack`.

## Install

Claude Code:

```sh
claude plugin marketplace add AISG-AIAP/aixtech-skills
claude plugin install pstack-starter@aixtech-skills
```

Codex:

```sh
codex plugin marketplace add AISG-AIAP/aixtech-skills
codex plugin add pstack-starter@aixtech-skills
```

Any other harness: copy or symlink every directory under `plugins/pstack-starter/skills/` into the harness's skills directory. Keep them as siblings, because `pstack` reads the other skills and the principles at `../<name>/SKILL.md`.

## Differences from upstream

- Only the Feature, Babysit, and Shipping playbooks are included. The Feature playbook's last step pushes and opens a PR instead of running the Opening a PR playbook.
- `how`, `architect`, `arena`, and `interrogate` are ported in full with their `references/` files. `why`, `unslop`, and `show-me-your-work` are short inline workflows in the **Workflows** section of `skills/pstack/SKILL.md`.
- Cursor-specific mechanics are replaced with neutral wording or removed. `poteto-agent`, the `Task` tool, `AskQuestion`, `/setup-pstack` model lines, and `agent-transcripts/` are reworded. Cloud agents, UI-testing control skills (`control-ui`, `control-cli`), `/loop`, the Origin forge, and Bugbot are removed.
- Babysit and Shipping use `gh` as the only forge. Babysit's sentences about the Autopilot playbooks are removed. Upstream's `watch-pr` script is removed, so the playbooks describe what to wait for and the agent does the watching itself.
- `references/code-review-triage.md` is upstream's `bugbot-triage.md`, rewritten for any code reviewer, bot or person.
- `principle-prove-it-works` points at the `show-me-your-work` workflow in `skills/pstack/SKILL.md` instead of a separate skill. The other principles are verbatim.

## Checking the plugin

```sh
python3 scripts/check-plugins.py
```

It fails when a plugin references a principle, skill, playbook, workflow, `references/` path, or relative link that the plugin does not include, or when a plugin is missing from either marketplace file.

## License

MIT. See `LICENSE`. The upstream copyright belongs to Lauren Tan.
