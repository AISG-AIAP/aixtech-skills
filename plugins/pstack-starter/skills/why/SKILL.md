---
name: why
description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Searches git history, pull requests, and GitHub Issues in parallel, then returns a cited read on decisions and tradeoffs. Use how for runtime behavior."
disable-model-invocation: true
---

# Why

Investigate the motivation and intent behind code. The companion `how` skill answers what the code does and how it works. `why` answers what forces led to its shape.

Every spawn is a subagent that can run `git` and `gh`. Investigators run on your fast code model and the synthesizer on your strongest judgment model, per the Subagents section of the [pstack](../pstack/SKILL.md) skill. When the harness offers no model choice, all run on the parent model. No spawn writes anything.

## Operating Posture

Operate as a **careful, cautious, and precise investigator**. Be honest about what you know vs what you're inferring. Read `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the Target and the Question

The **target** is usually a chunk of code, a pattern, a feature, or a named design decision. The **question** is usually a design rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a broad history sweep.

If the target is vague ("why do we do it this way?" with no clear referent), make your best guess from conversation context (open files, recent edits, cursor location, what was just discussed). State your interpretation briefly so the user can redirect if you're off, then proceed.

## Step 2. Establish the Code Anchor

Before spawning investigators, build the seed context inline: file paths and line ranges, key symbols (functions, classes, constants), the last few commits touching the target, PR numbers from merge commits (pattern `(#1234)` in the subject line), and any linked ticket IDs. Run `git blame -L <start>,<end> <file>` for last-touch commits, `git log --follow -p -- <file>` for full history with patches through renames, `git log --oneline -20 -- <file>` for recent commits with PR numbers visible, and `git log -1 --format=%B <commit>` to extract PR numbers. Then pull the PR bodies and discussion for any substantive commit: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`. This anchor goes to every investigator and to the synthesizer.

## Step 3. Spawn Parallel Investigators

**Default to the full parallel investigation.** The goal is a complete coverage map, not a minimal one. Document the null, don't skip the search.

### Discovery

This setup can search two evidence categories, both through git and `gh`:

1. Source control history
2. Issue / ticket tracker (GitHub Issues)

Five other categories are not available here: long-form documents, real-time team chat, infrastructure observability, error / exception tracking, and the product analytics warehouse. Record each one as a gap in Sources Consulted, not a choice.

Spawn one investigator per category, both at once so they run concurrently, each owning exactly one source.

Each investigator's prompt is `references/investigator-prompt.md` filled in, plus:
- the category playbook from `references/source-playbook.md`
- `references/sources/incident-postmortem.md` **if the target code looks defensive** (null checks, retry logic, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
- the code anchor and the user's original question

### Investigator roster

Each category below is uniquely positioned to surface one shape of "why", shown after "Best at". Use it to know what to expect back, to name a gap when a category returns empty, and, only in the rare provably-irrelevant case, to justify a skip.

1. **Source control** (git history, `gh` for PRs, code comments, tests). Always spawn, the only guaranteed source. Best at *implementation-time rationale captured during review*.
2. **Issue / ticket tracker** (GitHub Issues through `gh`). Best at *the product or business forcing function*. Strongest when the why is external to engineering.

### When to skip an investigator

Only with an **explicit, written justification** that goes in the final Sources Consulted. Two valid reasons:

- **The source is unavailable.** The repo has GitHub Issues turned off, or `gh` cannot reach it. Flag it as a gap, not a choice: "Issue tracker skipped. GitHub Issues is disabled for this repo, so ticket history was not searchable."
- **The source is provably irrelevant**, not just "probably irrelevant." A high bar: "Issue tracker skipped. Target is a vendored file copied verbatim from an upstream project."

If your scope assessment suggests a single-commit trivial target where the PR description already contains the complete answer, you may answer inline **only after** confirming both category searches would be redundant. Say so explicitly. This should be rare.

## Step 4. Synthesize

Spawn one synthesizer. It gets:
1. The investigator findings, including any null results and any categories skipped with justification
2. The code anchor
3. The user's original question
4. The epistemics framework from `references/epistemics.md`
5. The synthesizer prompt template from `references/synthesizer-prompt.md`

## Step 5. Present

Present the synthesizer's output to the user. You may lightly edit for clarity or add context from the conversation, but **do not rewrite the confidence language**.

## Output Format

The structure is the one in `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Adapt as needed, but keep the confidence separation intact, and keep Sources Consulted as one line per investigator, including the ones that returned nothing or were skipped, with the reason.

After Sources Consulted, if the user's `why` question is a precursor to changing this code, convert the lineage findings into a Preserve / Change / Avoid / Risk constraint set for planning the change.

## Common Failure Modes to Avoid

- **Recency bias**. Assuming the most recent commit is authoritative. The current shape is often the accretion of many earlier decisions. Trace back.
