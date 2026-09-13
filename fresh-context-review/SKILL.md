---
name: fresh-context-review
description: Run an independent fresh-context review loop with a subagent before finalizing code, design, documentation, or other substantial work. Use when the user asks for a fresh review, independent review, subagent review, pass/block diagnosis, review loop, or wants another agent to check whether the current work is acceptable before continuing.
---

# Fresh Context Review

## Overview

Use this skill to get an independent review from a fresh subagent, verify the findings locally, apply only verified fixes, and repeat until the work passes or the loop exposes a deeper issue that needs user attention.

The reviewer is an evaluator, not an authority. Treat every finding as a claim to verify.

## Preconditions

- Use this skill only when subagent tools are available and the user has explicitly requested this kind of independent review, directly or through an established user-approved workflow such as `$create-plan`. Do not ask again when that workflow already requires the review.
- If subagent tools are unavailable, do not simulate a fresh review. Report that the review loop is blocked.
- Keep the reviewer read-only unless the user explicitly asks for delegated edits.
- Do not use this skill for trivial changes where normal local verification is enough.

## Review Scope

Before spawning the reviewer, define the smallest useful review packet:

- user request and accepted constraints
- relevant files, diffs, design docs, schemas, or command outputs
- expected behavior and non-goals
- verification commands already run and their results
- specific questions the reviewer should answer

For workspace-backed work, record a local status/diff baseline before the review so unauthorized reviewer edits can be identified later. Prefer concrete commands such as `git status --short` and `git diff` when the target is a Git worktree.

Pass raw artifacts and objective constraints. Do not pass your suspected bugs, intended fixes, hidden conclusions, or the answer you want the reviewer to reach.

## Subagent Contract

Spawn one fresh reviewer at a time unless the user asks for parallel independent reviews.

- Use the available subagent tools directly and follow their current schemas rather than assuming a particular API version.
- Use the default agent type unless a specific reviewer role is clearly better.
- Do not override the model; let the subagent inherit the current model.
- Disable conversation inheritance: for example, use `fork_turns: "none"` when the spawning tool exposes that field, or `fork_context: false` when it exposes that field. Fresh context is the point of the skill.
- Give only the review packet, not the full conversation.
- Ask the reviewer for a read-only report.
- Wait for the report only when you are ready to evaluate it.
- Close the subagent immediately after receiving the report or after deciding it is unusable.

Where this skill says to close an agent, use the available lifecycle tools: close it if supported, interrupt an unusable running agent if supported, or let a finished agent remain idle when no close operation exists. Never invent a close tool. Use a new agent for each fresh review round rather than resuming a reviewer with prior-round context.

Treat a report as ungrounded when material claims lack concrete evidence such as file paths, line references, command output summaries, artifact excerpts, or explicit reasoning tied to the review packet.

If the reviewer times out, gives an ungrounded report, edits files without permission, or cannot evaluate the packet, close it and decide whether to retry with a clearer packet or escalate to the user.

If a reviewer was supposed to be read-only but changed files:

- close the reviewer
- inspect status and diffs before continuing
- do not silently incorporate unauthorized edits
- keep verified findings separate from unauthorized file changes
- ask the user before any destructive cleanup in a shared workspace

## Reviewer Report Format

Ask the reviewer to respond with this structure:

```text
Verdict: PASS | PASS_WITH_NOTES | BLOCK

Blocking Findings:
- [required for BLOCK] Concrete issue, why it blocks, and evidence.

Minor Findings:
- Non-blocking issue, cleanup, or risk.

Evidence:
- File paths, line numbers, command output summaries, or concrete artifact references.

Suggested Next Action:
- Minimal next step.
```

Use these verdict meanings:

- `PASS`: no material issue found.
- `PASS_WITH_NOTES`: only minor, non-blocking issues remain.
- `BLOCK`: correctness bug, contract violation, missing required behavior, failing verification, unsafe assumption, or unresolved edge case.

## Local Verification

After the reviewer reports:

1. Close the subagent.
2. Check each finding against source files, diffs, tests, commands, docs, or project constraints.
3. Mark each finding as verified, rejected, or inconclusive.
4. Fix only verified blocking findings and verified worthwhile minor findings.
5. Do not change code or docs for unverified claims.
6. If the reviewer missed an obvious issue found locally, include it in the next review packet.

When rejecting a finding, keep a short reason so the final report can distinguish reviewer claims from verified facts.

## Review Loop

Use this default loop:

1. Build the review packet.
2. Spawn a fresh reviewer.
3. Receive the report.
4. Close the reviewer.
5. Verify findings locally.
6. Apply verified fixes.
7. Run relevant local verification.
8. Repeat with the updated diff and verification results.

Default loop cap: 3 review rounds.

Stop early when:

- the reviewer returns `PASS`
- the reviewer returns `PASS_WITH_NOTES` and all notes are non-blocking or intentionally deferred
- no verified findings remain after local verification
- further changes would expand beyond the user-approved scope

## Escalation Rules

Pause the loop and report to the user when:

- the same blocking class appears in two review rounds
- three rounds complete without reaching pass
- the review target drifts beyond the original scope
- fixes are making the design more complex without improving the contract
- assumptions, requirements, constraints, or architecture appear wrong
- a necessary decision depends on user preference or domain knowledge

When escalating, include:

- what was reviewed
- what passed
- verified blocking findings
- rejected or inconclusive reviewer claims
- why the loop should stop
- the specific decision or redesign question for the user

## Final Report

When the loop ends successfully, report:

- final verdict
- number of review rounds
- verified issues fixed
- rejected or inconclusive reviewer claims, if relevant
- minor notes left intentionally unfixed, if any
- verification commands run
- remaining risk

Keep the report concise and grounded in verified facts.
