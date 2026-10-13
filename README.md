# aixtech-skills

Agent skills for aixtech, at <https://github.com/AISG-AIAP/aixtech-skills>. The repo is a plugin marketplace for Claude Code and Codex. Each plugin's `skills/` directory also works in any harness that reads Agent Skills.

| Plugin | Contents |
|---|---|
| `pstack-starter` | `/pstack` with the Feature, Babysit, and Shipping playbooks, the `how`, `architect`, `arena`, and `interrogate` skills Feature uses, the `/teach` skill, and the 17 principles they need. The first level of the course. |

## pstack-starter

`pstack-starter` is a harness-agnostic port of part of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, taken from upstream commit `1dcc2ba`.

- `plugins/pstack-starter/skills/pstack` is the single entry point, upstream's `/poteto-mode` renamed and trimmed to this level. It routes each task to a playbook in `skills/pstack/playbooks/` and grounds every decision in the principles.
- `plugins/pstack-starter/skills/how`, `architect`, `arena`, and `interrogate` are the skills the Feature playbook uses.
- `plugins/pstack-starter/skills/teach` explains a body of work so a person understands it. Invoke it with `/teach`.
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

## License

MIT. See `LICENSE`. The upstream copyright belongs to Lauren Tan.
