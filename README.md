# aixtech-skills

Agent skills for aixtech, at <https://github.com/AISG-AIAP/aixtech-skills>. The repo is a plugin marketplace for Claude Code and Codex. Each plugin's `skills/` directory also works in any harness that reads Agent Skills.

| Plugin | Contents |
|---|---|
| `pstack-starter` | `/pstack` with the Feature, Babysit, Shipping, and Opening a PR playbooks, the `how`, `why`, `architect`, `arena`, and `interrogate` skills Feature uses, the `technical-writing` and `/blast-radius` skills Opening a PR uses, the `/teach` and `/unslop` skills, and the 17 principles they need. The first level of the course. |
| `pstack-practitioner` | Everything in `pstack-starter`, plus the Investigation, Bug fix, and Prototype playbooks, the `tdd` skill, and the `/create-verification-skill` and `/maintain-verification-skill` skills. The second level. |

## pstack-starter

`pstack-starter` is a harness-agnostic port of part of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, taken from upstream commit `1dcc2ba`.

- `plugins/pstack-starter/skills/pstack` is the single entry point, upstream's `/poteto-mode` renamed and trimmed to this level. It routes each task to a playbook in `skills/pstack/playbooks/` and grounds every decision in the principles.
- `plugins/pstack-starter/skills/how`, `why`, `architect`, `arena`, and `interrogate` are the skills the Feature playbook uses. `why` searches git history, pull requests, and GitHub Issues.
- `plugins/pstack-starter/skills/teach` explains a body of work so a person understands it. Invoke it with `/teach`.
- `plugins/pstack-starter/skills/unslop` cuts AI tells from writing. `/pstack` and `/teach` write through it, and you can invoke it with `/unslop`.
- `plugins/pstack-starter/skills/principle-*` holds the 17 principles those skills and playbooks cite.

Invoke it with `/pstack` in Claude Code (`/pstack-starter:pstack` also works). Codex prefixes plugin skills with the plugin name, so there it is `$pstack-starter:pstack`.

## pstack-practitioner

`pstack-practitioner` contains everything in `pstack-starter` and adds:

- The Bug fix and Prototype playbooks. Both drive the app through the project's verification skill.
- The Investigation playbook, for read-only questions answered from `how` and `why` with citations.
- `tdd`, which Bug fix uses to land a failing test before the fix when the test is cheap.
- `create-verification-skill`, which writes a project-local skill at `.agents/skills/verify-<app>/` that launches the app, drives it the way a user does, and captures evidence.
- `maintain-verification-skill`, which audits that skill and its feature map against the current app.

Invoke it with `/pstack` in Claude Code. In Codex it is `$pstack-practitioner:pstack`.

## Install

Claude Code:

```sh
claude plugin marketplace add AISG-AIAP/aixtech-skills
claude plugin install pstack-starter@aixtech-skills
# next level
claude plugin uninstall pstack-starter@aixtech-skills
claude plugin install pstack-practitioner@aixtech-skills
```

Codex:

```sh
codex plugin marketplace add AISG-AIAP/aixtech-skills
codex plugin add pstack-starter@aixtech-skills
# next level
codex plugin remove pstack-starter@aixtech-skills
codex plugin add pstack-practitioner@aixtech-skills
```

Any other harness: copy or symlink every directory under one plugin's `skills/` folder into the harness's skills directory. Keep them as siblings, because `pstack` reads the other skills and the principles at `../<name>/SKILL.md`.

## License

MIT. See `LICENSE`. The upstream copyright belongs to Lauren Tan.
