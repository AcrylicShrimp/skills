# Shared Plan Contract

This document defines the common file format and lifecycle for `create-plan` and `implement-plan`. Maintain this contract and the sibling `../assets/plan-template.md` together. Do not duplicate them in the implementation skill.

## Unit of Work

A plan file represents exactly one implementation step: one bounded outcome with its own verification. It may change several files when they participate in that outcome. Do not put an implementation roadmap or multiple independently executable steps inside one file.

When work needs several steps, create several plan files and connect them with `Depends on` links. Do not add a second task-status document to coordinate them. Explicit dependencies determine execution order; daily filename counters do not. References for background information are not execution dependencies.

## File Format

Path: `REPO_ROOT/docs/plans/YYYY-MM-DD.NN.task-name.md`.

Use the local current date and a two-digit daily counter starting at `00`. Keep filenames stable after creation. Preserve all sections from the template, along with any existing review history and execution results. A plan is an English Markdown document, not a TODO document; do not pass it to either TODO script.

The fixed sections are:

- `Current Status`
- `Goal and Scope`
- `References and Dependencies`
- `Completion Criteria`
- `Proposed Changes`
- `Pseudo Code Diff`
- `Verification Plan`
- `Fresh Context Review`
- `Execution Result`
- `Plan Changes`
- `Follow-ups`

## Required Pseudo Code

Every plan must contain substantive pseudo code that a human can review. Do not replace it with a prose-only summary, a placeholder, or `Not applicable.`

For code changes, show affected paths, types and function signatures, contract changes, and the important success and failure flows. Prefer a high-level fenced `diff` block with `+`, `-`, and `~` markers. Keep bodies shallow, usually no more than two levels of nesting, and use meaningful helpers for deeper detail. Do not reproduce a complete implementation or invent APIs without checking the relevant source or documentation.

For documentation, configuration, or investigative work, use a structured before/after sketch, schema, or algorithm showing the concrete edit or procedure and its observable result. It must still make the proposed work reviewable rather than serving as decorative pseudo code.

## State and Readiness

Use exactly these plan states:

| State | Meaning |
| --- | --- |
| `Draft` | The proposal is being written, revised, or reviewed and is not ready to execute. |
| `Ready` | The final proposal passed fresh-context review and contains no unresolved planning blocker. Execution dependencies may still be pending. |
| `In Progress` | Authorized implementation has begun. |
| `Blocked` | Progress cannot continue because of a concrete dependency, missing capability, failed verification, or unresolved decision. |
| `Completed` | The completion criteria are fulfilled and the required verification and document updates are recorded. |
| `Dropped` | The objective was abandoned or replaced; the reason and any replacement link are recorded. |

`Ready` describes the proposal's quality; it is not user authorization to change code. Honor implementation authorization already present in the conversation instead of asking again.

Update `Last Updated` when changing the document. `Blocker` is `None` when there is no blocker; otherwise state the concrete condition and what would clear it. Keep the reason for a dropped plan in `Plan Changes`.

For readiness, the current review verdict must be `PASS`, or `PASS_WITH_NOTES` with all remaining notes verified as non-blocking and explicitly recorded. Never use `Ready` with `Pending`, `BLOCK`, unresolved material findings, unreviewed substantive edits, or unresolved architectural decisions. A reviewer returning `PASS` does not override a planning blocker the author can demonstrate.

Missing subagent capability before any execution leaves the file in `Draft` with a concrete blocker. An interrupted implementation uses `Blocked` when it cannot safely continue. Once a blocker clears, verify the current proposal, review, and implementation state before resuming; do not restart completed work blindly.

## Review Evidence and Invalidation

Use `Pending`, `PASS`, `PASS_WITH_NOTES`, or `BLOCK` for the current review verdict. Preserve a concise history under `Findings and Resolution`, including reviewer agent ID, round, verdict, concrete findings, their verified/rejected/inconclusive disposition, and the resulting action.

Identify the substantive proposal that was reviewed using an available revision, a saved review report tied to that content, or a concise description of the reviewed content and last substantive change. Do not claim a review of final content based on a review of an earlier proposal. Do not require a Git commit solely to identify a review.

Changes to the goal, scope, completion criteria, dependencies, contracts, pseudo code, or verification plan invalidate the current passing verdict. Record the reason under `Plan Changes`, mark the review `Pending`, and run a new fresh-context review before executing the changed proposal. A material revision during implementation suspends further affected edits; preserve partial results and mark the plan `Blocked` until the revised proposal is reviewed and safe to resume.

Progress updates, marking an already-defined criterion as fulfilled, recording verification output, fixing spelling, or adding execution evidence do not by themselves invalidate the proposal review.

The fresh-context loop is bounded by the review skill. If it stops without a passing review, retain the honest state and findings. Do not relabel a failed review as a pass or enter an unbounded loop.

## Execution and Closeout

`Execution Result` starts as `Not started.` During execution, record actual changes, verification commands or manual observations and outcomes, relevant commits or artifacts when available, partial progress, and remaining work. Distinguish checks not run from checks that passed. Keep enough evidence to resume from another session; do not copy the entire conversation.

Mark a plan `Completed` only when its completion criteria have been checked against actual results, required verification has passed, and relevant documentation reflects the outcome. An implementation mismatch with the reviewed design requires reconciliation, not an automatic rewrite of the design to match the code.

Link deferred work to `docs/todos` when appropriate. Deferring a required criterion does not satisfy it. If a source TODO is linked, update its evidence and mark it finished only when that TODO's own criteria are met, potentially after several plans. Plan review completion alone never completes an implementation TODO.

When a completed dependency changes materially, assess its effect on dependent plans' assumptions, contracts, and evidence before continuing them. A `Completed` label does not prove the prerequisite still holds in the current checkout.
