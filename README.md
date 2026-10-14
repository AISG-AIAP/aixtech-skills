# aixtech-skills

Agent skills for aixtech, at <https://github.com/AISG-AIAP/aixtech-skills>. The repo is a plugin marketplace for Claude Code and Codex. Each plugin's `skills/` directory also works in any harness that reads Agent Skills.

The plugins are levels of a course built on [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, ported from upstream commit `1dcc2ba` to work in any harness. Each level contains everything in the level before it. Every level has one entry point, `/pstack`, which routes each task to a playbook and grounds every decision in the principles.

| Level | Plugin | Playbooks | Skills | Principles |
|---|---|---|---|---|
| 1 | `pstack-starter` | 4 | 9 | 17 |
| 2 | `pstack-practitioner` | 7 | 13 | 17 |
| 3 | `pstack-expert` | 15 | 17 | 19 |

## Level 1: pstack-starter

Build a feature and get it merged.

Playbooks:

| Playbook | Use it for |
|---|---|
| Feature | New or changed behavior, built from a named data shape. |
| Opening a PR | Committing, writing the PR, and opening it. Every other playbook ends here. |
| Babysit | Driving a PR or a stack to merge-ready: conflicts, review threads, CI. |
| Shipping | Independently verifying a green stack, then landing it bottom-up through `gh`. |

Skills:

- `pstack`, the entry point.
- `how`, `why`, `architect`, `arena`, and `interrogate`, which Feature uses. `why` searches git history, pull requests, and GitHub Issues.
- `technical-writing` and `blast-radius`, which Opening a PR uses.
- `unslop`, which cuts AI tells from writing.

Principles: the 17 that these skills and playbooks cite. Boundary Discipline, Build the Lever, Encode Lessons in Structure, Exhaust the Design Space, Fix Root Causes, Foundational Thinking, Guard the Context Window, Laziness Protocol, Make Operations Idempotent, Minimize Reader Load, Model the Domain, Outcome-Oriented Execution, Prove It Works, Redesign from First Principles, Separate Before Serializing Shared State, Sequence Work into Verifiable Units, and Subtract Before You Add.

Invoke it with `/pstack` in Claude Code (`/pstack-starter:pstack` also works). Codex prefixes plugin skills with the plugin name, so there it is `$pstack-starter:pstack`.

## Level 2: pstack-practitioner

Everything in level 1, plus understanding code, fixing bugs, and prototyping against the running app.

Playbooks added:

| Playbook | Use it for |
|---|---|
| Investigation | Read-only questions: how does X work, why was Y built this way, should we do X or Y. |
| Bug fix | A reported defect to reproduce, root-cause, and fix with runtime evidence. |
| Prototype | A throwaway sketch to settle a design or behavior question by observing it. |

Skills added:

- `teach`, which explains a body of work as an HTML page, at the learner's pace. It uses `how` and `why`, like Investigation.
- `tdd`, which Bug fix uses to land a failing test before the fix when the test is cheap.
- `create-verification-skill`, which writes a project-local skill at `.agents/skills/verify-<app>/` that launches the app, drives it the way a user does, and captures evidence. Bug fix and Prototype drive the app through it.
- `maintain-verification-skill`, which audits that skill and its feature map against the current app.

Principles added: none. The new playbooks and skills cite only principles level 1 already has.

Invoke it with `/pstack` in Claude Code. In Codex it is `$pstack-practitioner:pstack`.

## Level 3: pstack-expert

Everything in level 2, plus refactoring, performance work, long-running work you can leave and audit later, and writing your own skills.

Playbooks added:

| Playbook | Use it for |
|---|---|
| Refactoring | A behavior-preserving change to structure or shape. |
| Perf issue | A measured slowness to trace and improve against a baseline. |
| Hillclimb | Sustained improvement of one metric against a target. |
| Autonomous run | Driving a long task to completion without stopping. |
| Session pickup | Resuming a prior agent's in-flight work. |
| Pause safely | Suspending work cleanly so it can be resumed. |
| Eval | Testing how a skill or prompt change affects agent behavior. |
| Authoring or modifying a skill | Writing or editing a SKILL.md. |

Skills added:

- `benchmark-checklist`, which vets a performance number before you trust or report it. Perf issue and Hillclimb use it.
- `show-me-your-work`, which keeps a decision log for work you review after stepping away. Autonomous run and Hillclimb use it. Levels 1 and 2 carry a short inline version in `/pstack` instead.
- `figure-it-out`, which designs a bespoke playbook for large work, and for any task no other playbook fits.
- `correct`, which finds mistakes agents keep repeating in a repo and makes each one impossible with architecture, types, a lint, or a test.

Principles added: Migrate Callers Then Delete Legacy APIs, which Refactoring cites, and Never Block on the Human, which `figure-it-out` cites.

Invoke it with `/pstack` in Claude Code. In Codex it is `$pstack-expert:pstack`.

## Install

Install one level at a time. To move up, uninstall the current level, then install the next.

Claude Code:

```sh
claude plugin marketplace add AISG-AIAP/aixtech-skills
claude plugin install pstack-starter@aixtech-skills
# next level
claude plugin uninstall pstack-starter@aixtech-skills
claude plugin install pstack-practitioner@aixtech-skills
# next level
claude plugin uninstall pstack-practitioner@aixtech-skills
claude plugin install pstack-expert@aixtech-skills
```

Codex:

```sh
codex plugin marketplace add AISG-AIAP/aixtech-skills
codex plugin add pstack-starter@aixtech-skills
# next level
codex plugin remove pstack-starter@aixtech-skills
codex plugin add pstack-practitioner@aixtech-skills
# next level
codex plugin remove pstack-practitioner@aixtech-skills
codex plugin add pstack-expert@aixtech-skills
```

Any other harness: copy or symlink every directory under one plugin's `skills/` folder into the harness's skills directory. Keep them as siblings, because `pstack` reads the other skills and the principles at `../<name>/SKILL.md`.

## License

MIT. See `LICENSE`. The upstream copyright belongs to Lauren Tan.
