---
name: create-todo
description: Create temporary, near-term blocked action-item markdown files and keep a structured execution log. Use when work must be tracked for follow-up because it is blocked by current priorities, dependencies, or unresolved issues, and you need a standardized TODO file at repository-root/docs/todos/YYYY-MM-DD.NN.name-of-the-task.md.
---

# Create Todo

## Overview

Create a TODO markdown file for blocked near-future work with a strict filename pattern, mandatory status fields, and structured activity logs.

Use `scripts/create_todo.py` for deterministic file naming and template generation.

## Workflow

1. Capture the task title and normalize scope.
2. Create the TODO file with `scripts/create_todo.py`.
3. Fill or refine context, justification evidence, completion criteria, and detailed plan.
4. For TODOs that include code changes, add a pseudo code diff before implementation starts.
5. Append activity logs for each logical action group using `USER`, `ACTION`, `RESULT`.

Use `$update-todo` to continue or revise the resulting file. Pass its exact path and preserve its completion criteria, pseudo code diff, and existing activity log; do not create a duplicate tracker for the same objective.

## File Naming Rules

- Target path: `repository-root/docs/todos/YYYY-MM-DD.NN.name-of-the-task.md`
- `YYYY-MM-DD`: local current date.
- `NN`: zero-padded counter from `00` to `99`, scoped per date.
- `name-of-the-task`: lowercase hyphen-case slug derived from title.

## Content Schema

Use this exact section structure:

1. `## Current Status`
- `State`: one of `Not Yet Started`, `Partially Taken`, `Finished`, `Dropped`
- `Dropped Reason`: required only when state is `Dropped`
- `Last Status Update`: datetime in `YYYY-MM-DD HH:MM:SS`

2. `## Context`
- Describe relevant background and blockers.

3. `## Why It Is Needed`
- State justification with concrete evidence when available.

4. `## Completion Criteria`
- Define objective done conditions.

5. `## Detailed Plan`
- Leave blank when not ready.

6. `## Pseudo Code Diff`
- Required when the TODO includes code changes.
- Use a high-level code-shaped pseudo-diff, not an exact patch, unless the exact patch is already known.
- Include intended file/module boundaries and contract changes.
- Prefer pseudo signatures, type shapes, function names, control-flow sketches, and API call ordering over prose descriptions.
- Include enough detail that a future implementation can preserve intended contracts without rediscovering the design.
- Keep function bodies shallow. When sketching function logic, stop after two levels of nesting or decomposition and summarize deeper logic behind helper names, comments, or ellipses.
- Do not expand loops, matches, branches, or helper internals when doing so would make the pseudo diff read like implementation code.
- Avoid import statements unless they are essential to communicate a new dependency, public module boundary, or non-obvious external API contract.
- Prefer fenced `diff` blocks with `+`, `-`, and `~` markers.
- Use prose inside the diff only as short comments attached to code-like structures.
- For TODOs with no code changes, write `Not applicable.`

7. `## Activity Log`
- Use bullet entries with exact format:
  - `[YYYY-MM-DD HH:MM:SS] [CATEGORY] Log item detail`
- Allowed categories only:
  - `USER`: cleaned summary of user request/instruction/notable intent
  - `ACTION`: action taken
  - `RESULT`: consequence/outcome of action

## Activity Log Policy

- Add log entries for every logical action group.
- Prefer logging one `USER`, one `ACTION`, and one `RESULT` entry per group.
- Keep logs factual and concise; avoid raw internal reasoning.

## Commands

Create a basic TODO:

```bash
python3 ~/.codex/skills/create-todo/scripts/create_todo.py "Integrate payment webhook retries"
```

Create with explicit content:

```bash
python3 ~/.codex/skills/create-todo/scripts/create_todo.py "Integrate payment webhook retries" \
  --status not-started \
  --context "Webhook retries are blocked by missing idempotency key strategy." \
  --why-needed "Failed deliveries currently require manual replay; evidence from incident INC-204." \
  --completion-criteria "- [ ] Retries are idempotent\n- [ ] Duplicate side effects are prevented\n- [ ] Runbook updated" \
  --detailed-plan "" \
  --pseudo-code-diff "Not applicable." \
  --user-note "Track blocked webhook retry implementation as a near-term action item." \
  --action-note "Created TODO tracker file for blocked webhook retries." \
  --result-note "Follow-up artifact is now tracked in docs/todos."
```

Create a code-change TODO with pseudo code diff:

```bash
python3 ~/.codex/skills/create-todo/scripts/create_todo.py "Refactor recipe pipeline contracts" \
  --context "Recipe pipeline stages need explicit type boundaries before implementation expands." \
  --completion-criteria "- [ ] Raw and validated data use distinct types\n- [ ] Graph resolution accepts only validated data" \
  --pseudo-code-diff $'```diff\n~ crates/aic-data/src/recipes.rs\n- impl RecipeBook { pub fn resolve_graph(&self, target: &str) -> Result<RecipeGraph, RecipeGraphError> }\n+ mod validated;\n+ pub use validated::ValidatedRecipeBook;\n\n+ crates/aic-data/src/recipes/validated.rs\n+ pub struct ValidatedRecipeBook { book: RecipeBook, index: RecipeIndex }\n+ impl ValidatedRecipeBook {\n+     pub fn try_from_recipe_book(book: RecipeBook) -> Result<Self, ValidationReport>;\n+     pub fn resolve_graph(&self, target: &str) -> Result<RecipeGraph, RecipeGraphError>;\n+ }\n\n~ crates/aic-cli/src/main.rs\n+ fn graph_recipes(file: PathBuf, target: String) -> Result<()> {\n+     let book = load_recipe_book(&file)?;\n+     let validated = ValidatedRecipeBook::try_from_recipe_book(book)?;\n+     write_json(validated.resolve_graph(&target)?)\n+ }\n```'
```

Create a dropped TODO:

```bash
python3 ~/.codex/skills/create-todo/scripts/create_todo.py "Legacy API migration" \
  --status dropped \
  --dropped-reason "Program canceled after architecture review on 2026-03-04."
```

## Script Reference

`scripts/create_todo.py`:

- Creates `repository-root/docs/todos/` when missing.
- Computes next same-date counter (`NN`) automatically.
- Enforces `--dropped-reason` when status is dropped.
- Adds a `Pseudo Code Diff` section; pass `--pseudo-code-diff` for code-change TODOs or use `Not applicable.` for non-code TODOs.
- Generates initial `USER`, `ACTION`, `RESULT` log entries.
