---
name: implement-plan
description: Execute or resume a reviewed implementation plan from docs/plans, treating one file as one implementation step and recording progress, verification, and completion in that file. Use when the user asks to implement or continue a plan. Check dependencies and fresh-context review before execution, and request a new review for substantive plan changes. Do not use to author a new plan from an unplanned request.
---

# Implement Plan

Execute the one step defined by the selected plan, preserving its reviewed contracts and keeping the document useful to the next session.

## Shared Contract

Read [the shared plan contract](../create-plan/references/plan-contract.md) before executing. The canonical [template](../create-plan/assets/plan-template.md) is owned by `$create-plan`; do not maintain a second schema here. Resolve these resources relative to the actual skill directory, following symlinks when necessary. Install `create-plan`, `implement-plan`, and `fresh-context-review` together. If the shared contract is unavailable, report the missing dependency rather than guessing its format.

## Select and Check the Plan

1. Read the target repository's instructions and identify the exact plan from the user's request and current context. If necessary, search `docs/plans` by title, state, and relevant terms. Ask only if multiple candidates remain plausible or none match.
2. Read the plan, its referenced design, any source TODO, required dependency plans, and the relevant current code and tests. A plan is documentation, not an executable script; do not run its pseudo code as a command.
3. Check the shared contract's readiness rules. A `Draft`, `Pending` review, blocking finding, or substantively stale review cannot authorize execution. Use `$create-plan` to revise and obtain the required fresh-context review when needed within the requested scope.
4. Confirm each execution dependency is `Completed` and its promised contract exists in the current checkout. Do not implement prerequisites merely because they are linked. If the user's request includes the dependency chain, execute those plan files in dependency order; otherwise report the unmet prerequisite on the selected plan.
5. Resume an `In Progress` or `Blocked` plan from actual code and recorded evidence, provided its proposal review is still valid and the relevant blocker is cleared. For a `Completed` plan, report its result without replaying it; treat a newly requested correction as new or explicitly reopened work. Do not revive `Dropped` work without user direction.

## Execute the Step

- Honor the implementation request already given. Do not ask for another approval merely because the plan was created or reviewed in another session.
- Set `State` to `In Progress`, clear a resolved blocker, and update the timestamp when execution begins or resumes.
- Implement only the selected file's bounded outcome. Follow its pseudo code as a reviewed contract, adapting ordinary implementation details to real APIs while preserving the intended behavior.
- Preserve unrelated work. Read actual file changes before resuming so already completed work is neither overwritten nor repeated.
- Update `Execution Result` at meaningful checkpoints with actual changes, verification outcomes, and unfinished work. Keep the original proposal and review history intact.
- If code, dependencies, or requirements invalidate the proposal, record the discrepancy and apply the contract's review-invalidation rules. Obtain a decision when an architectural or scope choice cannot be inferred from the request. Suspend affected implementation until the revised proposal is reviewed.
- Use `$pm-mode` only for delegation authorized by the user. A plan remains one step even when several files or helpers participate in its outcome; do not turn it into a multi-step roadmap during execution.

## Verify and Close

1. Run the planned checks and any additional checks justified by the actual change. Record expected versus observed results and distinguish unrun or failed checks from passing ones.
2. Reconcile relevant documentation with verified behavior. Record material departures from the agreed design explicitly; do not silently bless code by rewriting its design.
3. Record separately deferred work through `$create-todo` when appropriate and link it under `Follow-ups`. Update a linked source TODO through `$update-todo`, preserving its pseudo diff and previous evidence. Finish it only when its own criteria are satisfied.
4. Check off completion criteria only with evidence. Mark `Completed` only under the shared contract's closeout rules. If required work remains, retain `In Progress` or `Blocked` with a concrete next action instead of declaring success.
5. Return the plan path, final state, actual changes, verification results, and remaining blockers or follow-ups.

Fresh-context review is mandatory for the plan proposal. Independent review of the resulting implementation is a separate requirement: run it when requested, required by the plan, or required by repository instructions. Do not claim code review occurred merely because the plan was reviewed.
