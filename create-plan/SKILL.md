---
name: create-plan
description: Create human-reviewable implementation plans under docs/plans, with exactly one implementation step per file, required pseudo code, explicit dependencies, and a mandatory fresh-context agent review before readiness. Use when the user asks to write or revise an implementation plan or turn an agreed design or TODO into executable work. Do not use for implementation alone or unresolved architectural design discussions.
---

# Create Plan

Turn a sufficiently concrete request into a reviewed plan that another session can execute without rediscovering the intended contracts.

## Shared Contract

Read [the plan contract](references/plan-contract.md) and use [the plan template](assets/plan-template.md). These are also the source of truth for `$implement-plan`.

This workflow requires `$fresh-context-review` and actual subagent tools. The established workflow requires review after authoring; do not request a separate routine confirmation for that review. If review cannot run, retain the draft and report the missing capability. Never substitute the author's self-review or invent a passing verdict.

## Author the Plan

1. Read the target repository's instructions, relevant code, tests, and any supplied design or TODO. Locate its root from the actual project context; do not confuse the skill repository with the project receiving the plan.
2. Identify the single outcome and its boundaries. If important architectural choices remain unresolved, retain a `Draft`, name the open decisions, and use `$interactive-design-mode` when the user wants to settle the design. Do not present unresolved decisions as agreed contracts.
3. Use one file per implementation step. If the request needs several separately verifiable steps, create several files with explicit dependency links. Calls and control flow inside one step's pseudo code do not constitute additional implementation steps.
4. Write each file at `REPO_ROOT/docs/plans/YYYY-MM-DD.NN.task-name.md`, using the local date, the next unused two-digit counter starting at `00`, and a lowercase hyphen-case slug. Check existing files before writing and never overwrite a different plan. A filename counter is an identifier, not an execution order.
5. Fill the template with observable completion criteria, real file or module boundaries, required pseudo code, and verification commands or manual checks with expected outcomes. Write the plan in English. Use relative links between project documents. Design and source TODO links are optional; dependency links must identify exact files.
6. Keep planning edits within documentation. Creating a plan does not authorize implementing it. If the user already requested both planning and implementation, proceed to `$implement-plan` once this plan passes review and its dependencies are satisfied.

## Required Fresh Context Review

After writing the actual plan file, load `$fresh-context-review` and run its bounded review loop. Supply the user's request and accepted constraints, this plan contract, the plan file, relevant design and dependency files, and the minimum source and tests needed to evaluate it. Do not pass the author's preferred verdict or the full conversation.

Ask the fresh reviewer to check:

- The file contains exactly one implementation step and preserves the requested scope.
- The pseudo code lets a human understand the proposed contract and behavior, including relevant failure handling.
- The proposal fits the current code and agreed design; important assumptions are supported or explicitly unresolved.
- Completion criteria and verification can establish the promised outcome.
- Dependencies, review state, and links are coherent. Detect cycles across related plans.

Every plan file needs a recorded verdict. One review packet may include several related plan files to check their interfaces, but the reviewer must give findings and a verdict for each file.

Verify findings locally, fix supported issues, and have the final substantive content reviewed again after fixes. Record reviewer identity, the content reviewed, each round's verdict, finding dispositions, and remaining notes in `Fresh Context Review`. Use the readiness rules in the shared contract. Do not promote a plan merely because the author disagrees with a blocking reviewer; resolve the evidence through the review loop.

Return each plan's path, state, review outcome, dependencies, and unresolved issues. Creating a plan for a TODO does not complete that TODO; add a cross-reference using `$update-todo` when that tracker is part of the authorized work.

## Revise an Existing Plan

Preserve the plan's identity when refining the same objective. Record material changes under `Plan Changes`, retain previous review and execution evidence, and reset the current review to `Pending` before reviewing the revised proposal. If the objective changes entirely, preserve the old record as `Dropped` with a reason and link to a new plan rather than rewriting its history.
