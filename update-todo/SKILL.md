---
name: update-todo
description: Update existing TODO tracker files at repository-root/docs/todos with strict status and activity-log semantics. Use when a user asks to continue, revise, progress, complete, or drop an existing TODO item, and when ambiguity must be resolved before editing.
---

# Update Todo

## Overview

Update existing TODO files while preserving traceability.

If the active TODO item is ambiguous, stop and ask the user for clarification before making edits.

Use `scripts/update_todo.py` for deterministic section updates and activity-log appends.

## Canonical TODO Shape

Expect TODO files at:

- `repository-root/docs/todos/YYYY-MM-DD.NN.name-of-the-task.md`

Expected fixed labels and sections:

- `# TODO: ...`
- `## Current Status`
  - `- State:`
  - `- Dropped Reason:`
  - `- Last Status Update:`
- `## Context`
- `## Why It Is Needed`
- `## Completion Criteria`
- `## Detailed Plan`
- `## Pseudo Code Diff`
- `## Activity Log`

Preserve existing sections and their order, including `Pseudo Code Diff` and any additional sections. Treat headings inside fenced code blocks as content, not document sections. If a document has duplicate section names outside code blocks, report the ambiguity without overwriting it.

For code-change TODOs, maintain the high-level pseudo diff required by `$create-todo`. Use `Not applicable.` for non-code work. If the section is absent, add it when supplying the diff rather than discarding or rewriting other content.

Activity log line format:

- `- [YYYY-MM-DD HH:MM:SS] [CATEGORY] detail`

Allowed categories only:

- `USER`
- `ACTION`
- `RESULT`

## Discovery Workflow (Mandatory)

1. Identify the candidate TODO item from user context.
2. If the target is not explicit, search:

```bash
rg --files docs/todos | sort
rg -n "^# TODO:|^- State:|^- Last Status Update:" docs/todos
rg -n "<keyword-from-user>" docs/todos
```

3. If multiple candidates remain plausible, or none are relevant:
- Stop.
- Ask user which TODO file to update.

Do not guess when ambiguous.

## Update Workflow (Mandatory)

1. Update the selected TODO file using `scripts/update_todo.py`.
2. Keep status consistent with progress:
- `not-started` -> `Not Yet Started`
- `in-progress` -> `Partially Taken`
- `completed` -> `Finished`
- `dropped` -> `Dropped`
3. If `## Detailed Plan` is empty and a concrete plan is now available, immediately write that plan to the TODO file.
4. Always append activity logs for each logical action group.
- Prefer a `USER` + `ACTION` + `RESULT` set per update group.
5. Keep logs factual and concise.
6. Preserve the pseudo code diff unless the intended implementation changes. When it changes, update it explicitly with `--pseudo-code-diff`, following the same scope and detail rules as `$create-todo`.

## Scope/Target Change Policy (Mandatory)

If the user changes the TODO objective (context/target materially differs from original intent):

1. Do not rewrite the old TODO into a different objective.
2. Mark old TODO as dropped with explicit reason.
3. Create a new TODO for the new objective using `$create-todo`.
4. Add cross-reference notes in activity logs (old -> new, new <- old).

## Commands

Basic update with explicit status and triad logs:

```bash
python3 ~/.codex/skills/update-todo/scripts/update_todo.py \
  --file docs/todos/2026-03-04.00.example-task.md \
  --status in-progress \
  --user-note "User requested progress on retry integration todo." \
  --action-note "Updated status and preserved existing criteria." \
  --result-note "Todo status moved to Partially Taken."
```

Append additional structured logs:

```bash
python3 ~/.codex/skills/update-todo/scripts/update_todo.py \
  --file docs/todos/2026-03-04.00.example-task.md \
  --log USER "User confirmed blocker is resolved." \
  --log ACTION "Executed validation checks and updated detailed plan." \
  --log RESULT "Task is ready for completion review."
```

Apply a newly generated plan to an empty `## Detailed Plan` section:

```bash
python3 ~/.codex/skills/update-todo/scripts/update_todo.py \
  --file docs/todos/2026-03-04.00.example-task.md \
  --detailed-plan $'1. Finalize DTO contract\n2. Implement repository method\n3. Add controller and route\n4. Run fmt/clippy/tests' \
  --user-note "User approved implementation plan." \
  --action-note "Wrote generated plan into Detailed Plan section." \
  --result-note "TODO now contains executable step-by-step plan."
```

Update the implementation sketch without replacing the detailed plan:

```bash
python3 ~/.codex/skills/update-todo/scripts/update_todo.py \
  --file docs/todos/2026-03-04.00.example-task.md \
  --pseudo-code-diff $'```diff\n+ fn validate_input(raw: RawInput) -> Result<ValidatedInput>;\n```' \
  --action-note "Updated the implementation sketch to match the agreed contract." \
  --result-note "The TODO preserves the revised validation boundary."
```

Drop obsolete TODO before creating a new one:

```bash
python3 ~/.codex/skills/update-todo/scripts/update_todo.py \
  --file docs/todos/2026-03-04.00.old-target.md \
  --status dropped \
  --dropped-reason "Target changed to a different objective per user request." \
  --user-note "User changed target objective." \
  --action-note "Marked existing todo as dropped." \
  --result-note "Ready to create replacement todo with $create-todo."
```

Then create new TODO:

```bash
python3 ~/.codex/skills/create-todo/scripts/create_todo.py "new target objective"
```

## Script Reference

`scripts/update_todo.py`:

- Parses canonical TODO sections and validates required labels.
- Updates status fields and status timestamp.
- Enforces dropped reason when status is dropped.
- Replaces optional sections (`Context`, `Why It Is Needed`, `Completion Criteria`, `Detailed Plan`, `Pseudo Code Diff`) when provided.
- Preserves all other sections and their order, including fenced code content.
- Appends timestamped activity logs with category validation.
