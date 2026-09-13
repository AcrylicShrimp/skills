---
name: interactive-design-mode
description: Enter a discussion-first architecture mode for drafting, solidifying, reviewing, simulating, and stress-testing core system design before implementation. Use when the user wants to finalize architecture, harness design, prompt design, data flow, boundaries, protocol shape, or other foundational design decisions and explicitly wants consensus before code changes. In this mode, do not add, modify, or delete source code; only documentation edits are allowed, and concluded discussions should be captured as finalized design docs under REPO_ROOT/docs/designs.
---

# Interactive Design Mode

## Overview

Enter a design-only workflow for locking down core architecture before implementation. Use discussion, critique, simulation, and comparison to reach enough consensus that the next implementation steps are narrow and deliberate.

## Operating Rules

- Treat the session as design work, not implementation work.
- Do not add, modify, or delete source code while this mode is active.
- Allow documentation work only when it helps capture or refine the design.
- Push back on premature implementation requests until the design is sufficiently settled, unless the user explicitly exits the mode.
- Optimize for design clarity, boundary quality, and decision traceability rather than momentum through code changes.

## Workflow

1. Re-state the design target.
- Name the subsystem or architectural surface being designed.
- State the design objective in concrete terms.
- State the main constraints, invariants, and success criteria.

2. Build the current-state model.
- Read only the code and docs needed to understand the current architecture.
- Summarize the existing design in a small number of concrete points.
- Call out the specific mismatches, pain points, or ambiguities that motivate the rework.

3. Drive the design discussion.
- Propose candidate shapes, boundaries, schemas, or flows.
- Compare options directly and explain tradeoffs.
- Ask concise, high-value questions only when they materially affect the architecture.
- Prefer converging on explicit contracts over vague design language.

4. Stress-test the design.
- Simulate realistic turn flows, failure cases, edge cases, and extension points.
- Look for hidden mutable state, ownership confusion, invalidation hazards, ordering problems, and cache-hostile inputs.
- Challenge weak assumptions and revise the proposal when a stronger model is available.

5. Record consensus.
- Summarize what is agreed, what remains open, and what was rejected.
- Convert the agreed design into concrete action items or phased implementation slices.
- Update TODO files or design docs when that helps preserve the result.

## Discussion Style

- Keep the conversation active and collaborative; do not disappear into silent planning.
- Prefer concrete schemas, message shapes, state boundaries, and lifecycle descriptions over general opinions.
- Use examples and short simulated flows to validate the design.
- Separate facts about the current system from proposed changes and from open questions.
- When referencing external systems or frameworks, say explicitly whether the comparison is verified or inferred.

## Allowed Work

- Read code, docs, tests, schemas, and protocol definitions.
- Search external documentation when current behavior or public guidance matters.
- Draft design notes, TODO items, architecture docs, and decision records.
- Review existing designs for gaps, regressions, or contradictions.

## Disallowed Work

- Editing implementation files.
- Sneaking in “small” refactors before consensus exists.
- Converting unresolved design discussion into code prematurely.
- Treating an incomplete plan as if the architecture were already decided.

## Exit Criteria

Exit this mode only when one of these is true:

- The user explicitly says to leave design mode and start implementing.
- The core design has enough consensus that implementation slices are concrete, ordered, and low-ambiguity.
- The remaining uncertainty is small enough to defer safely into tracked follow-up items.

## Closeout

When the discussion is finished with enough consensus, and it is not terminated or dropped:

- Create a finalized design document at `REPO_ROOT/docs/designs/YYYY-MM-DD.NN.design-or-discussion-name.md`.
- Create `docs/designs/` if it does not already exist.
- Use the local current date for `YYYY-MM-DD`.
- Use a zero-padded daily counter for `NN`, starting at `00` and incrementing within that date.
- Use a lowercase hyphen-case slug for `design-or-discussion-name`.
- Treat the file as the canonical record of the concluded design discussion.

Do not create this finalized design doc when:

- the discussion is explicitly dropped
- the discussion is interrupted before enough consensus exists
- the user decides to postpone the design without concluding it

The finalized design doc should capture at least:

- the design goal
- the agreed architecture or model
- the key invariants and boundaries
- the important tradeoffs and rejected alternatives
- the remaining open issues, if any
- the concrete next implementation slice

## Handoff Output

When the design is solid enough, produce:

- the finalized design doc path, when one was created
- a bullet list that summarizes the conclusion
- the agreed architecture summary
- the key invariants and boundaries
- the open issues, if any
- the concrete next implementation slice
- any docs or TODO updates created during the discussion
