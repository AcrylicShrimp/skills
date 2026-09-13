---
name: pm-mode
description: Coordinate project-manager style delegation across multiple Codex threads. Use when Codex is asked to split upcoming work into several feature tasks, create or steer background/new Codex threads, assign each thread a bounded implementation or investigation scope, coordinate dependencies between threads, or manage cross-thread integration and review.
---

# PM Mode

Use this skill to plan and delegate project work across multiple Codex threads while keeping ownership boundaries explicit.

## Core Rules

- Keep the parent thread responsible for planning, boundary setting, integration, and final user communication.
- Use child threads for concrete, bounded work that can proceed independently.
- Write prompts to child threads in English, even if the user is speaking another language.
- Include repository rules, user constraints, current branch/worktree assumptions, and allowed write scope in every child-thread prompt.
- Tell child threads that other agents may be working in parallel and that they must not revert or overwrite unrelated changes.
- Do not delegate the immediate blocking decision if the parent thread needs that answer before it can plan safely.

## Decomposition

Before creating threads, make a short delegation map:

1. Identify the desired end state and verification criteria.
2. Split the work by feature, module, file set, ownership prefab, or other natural boundary.
3. Mark each slice as independent, dependent, or overlapping.
4. Assign each delegated slice a clear output: patch, analysis, test result, asset, or recommendation.
5. Keep shared architecture, shared API design, and final integration in the parent thread unless a single child thread is explicitly assigned that coordination role.

Prefer fewer, well-bounded threads over many tiny threads.

## Coordination

If two slices may touch the same files, Unity prefabs/scenes, shared APIs, migrations, package settings, generated artifacts, or runtime contracts, do not let child threads proceed independently without a coordination rule.

Use one of these patterns:

- **Serial dependency**: Thread B waits for Thread A's output or contract.
- **Explicit contract**: The parent defines the interface, files, data shape, or ownership boundary before both threads start.
- **Single owner**: Assign the shared surface to exactly one thread and make other threads consume it through the documented surface.
- **Parent integration**: Children produce isolated outputs; the parent applies or merges the shared change.

If a child thread discovers a boundary conflict or needs a shared change outside its assignment, instruct it to stop and report the required coordination instead of widening scope on its own.

## Creating Child Threads

When thread-management tools are available:

1. Use the current project when the work is repository-scoped.
2. Choose a local or worktree environment according to the user's request and the risk of parallel file edits.
3. Create one thread per independent slice.
4. Set a concise title when a title tool is available.
5. After creating threads, track their IDs, assigned scopes, and expected outputs in the parent thread.

For each child-thread prompt, include:

- The task objective.
- The exact allowed write scope, or state that it is read-only.
- Relevant repository or project rules.
- Expected final response format.
- Coordination instructions for overlap, dependencies, or unexpected shared changes.
- A reminder that the conversation must be in English.

## Prompt Template

Use this shape for child-thread prompts:

```text
You are working as one delegated Codex thread for a larger project. Communicate in English.

Repository/context:
- <repo path, branch/worktree assumptions, important project rules>

Your assigned scope:
- <files, modules, feature, prefab, or read-only area>

Task:
- <concrete objective>

Boundaries:
- Do not edit outside the assigned scope.
- Other agents may be working in parallel; do not revert unrelated changes.
- If you need a shared API, shared asset, or overlapping file change, stop and report the coordination need instead of widening scope.

Expected output:
- <changed files, tests run, findings, blockers, or patch summary>
```

## Integration

After child threads report back:

1. Review results against the original delegation map.
2. Verify claims locally when they affect correctness, shared contracts, or user-visible behavior.
3. Resolve overlaps in the parent thread or by assigning a single follow-up owner.
4. Run appropriate tests or verification for the integrated result.
5. Report to the user which threads were created, what each did, what remains blocked, and what was verified.
