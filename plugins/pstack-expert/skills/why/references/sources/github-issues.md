# GitHub Issues

## What this source contains

- Issues describing features, bugs, and their motivation
- Comments on issues (clarifications, scope changes, "why we're doing this" rationale)
- Labels (e.g., `compliance`, `customer-request`, `perf`) that signal the type of motivation
- Milestones that tie work to a release or deadline
- Linked pull requests and cross-references from other issues
- Tracking issues and task lists that group related work

GitHub Issues is where the product or business context often lives: the "we're doing this because customer X asked" or "this is for the Q3 compliance initiative" layer.

## How to search it

Use `gh`.

1. **Start with linked issues.** If the seed commits or PRs reference issues (`#1234`, `Fixes #567`, or the PR's closing issues), fetch those first with `gh issue view <number> --comments`. Read the full issue including comments.
2. **Search related issues by keyword.** Use `gh issue list --state all --search "<terms>"` or `gh search issues --repo <owner>/<repo> "<terms>"` for the feature name, key symbol, or business term. Try multiple phrasings.
3. **Walk up to the tracking issue.** If an issue is one item in a larger effort, find the tracking issue or task list that references it. Item issues are tactical. Tracking issues often carry the "why."
4. **Check labels and milestones.** Labels hint at the category of motivation (customer-request, incident-followup, compliance). Milestones tie work to deadlines, which often reveal motivation.

## What good evidence looks like here

- An issue description stating the business problem: "Customer Acme needs X because of their SOC2 audit"
- A comment recording a decision: "We decided to go with approach B because approach A would require touching the billing service"
- A tracking issue titled like an initiative: "Q3 Enterprise Readiness" or "Reduce Payment Failures"
- Labels like `customer:acme`, `incident-followup`, `compliance`, `perf-regression`

## Common pitfalls

- **Scope drift.** The issue the PR references may have been closed and reopened with a different scope. Read the whole history.
- **Mechanical templates.** Some teams require "Why" sections but fill them with boilerplate. Generic text ("improve user experience") is probably not a real answer.
- **Stale issues.** Old issues often reflect a version of the plan that changed. Check dates and cross-reference with the code's ship date.
- **Closed-as-duplicate chains.** Follow "duplicate of" references back to the canonical issue.
- **Issues disabled or private.** If the repo has issues turned off or you can't access an issue, note that as a gap rather than guessing.

## What to return

For each relevant issue:
- Issue number and title
- The problem/motivation quoted from the description or comments (not paraphrased. The synthesizer needs the exact text to cite)
- Labels, milestone, and tracking issue
- Author, created date, closed date
- Link to the issue
