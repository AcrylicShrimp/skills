# Personal Skills

This repository is intended to hold my personal Codex skills and keep them in sync across machines through Git. Each skill lives in its own directory, including its `SKILL.md` and any supporting scripts, references, or assets.

All imported skills must be in English. Non-English skills are translated during import while preserving their meaning and behavior. The detailed rules and agent procedures live in [AGENTS.md](AGENTS.md).

## Symlink layout

Keep the actual skill files in this repository and create a symbolic link for each skill directory inside the local Codex skills directory:

```text
<repository>/                     # Git working copy: actual files
├── README.md
├── AGENTS.md
├── baby-mode/
│   └── SKILL.md
└── create-todo/
    └── SKILL.md

<Codex skills directory>/         # Location used by your installation
├── .system/                       # Bundled skills, kept locally
├── baby-mode -> <repository>/baby-mode
└── create-todo -> <repository>/create-todo
```

This is the intended layout; the skill names are examples. Editing a file through either path changes the same file, and Git tracks changes in this repository.

The labels above represent your checkout and the skills directory used by your Codex installation. See the [official Codex documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) for supported skill locations and symlink behavior.

## Why link individual skills?

Link each skill directory instead of replacing the entire local skills directory with one symlink. This keeps bundled `.system` skills and any machine-specific skills separate from the repository.

Linking the entire directory would make newly added skills available without creating additional links, but it would also place local contents such as `.system` in the repository's working directory. Individual links provide more control over which skills are shared and enabled on each machine.

## Set up a machine

Clone the repository wherever you keep your projects:

```sh
git clone https://github.com/AcrylicShrimp/skills.git
cd skills
```

Identify the skills directory used by your Codex installation and create it if needed. Add a symlink there for each skill you want to use, pointing to that skill's directory in this checkout. You can also ask your coding agent to perform this setup using the prompts below.

If the destination already contains a skill directory, compare it with the repository version and preserve any local changes before replacing it with a link. Do not overwrite it blindly.

Symlinks are local setup: each machine creates its own links to its own checkout. Commit the actual skill files to Git, not the links in the local Codex skills directory.

## Ask an agent to set things up

After cloning, open this checkout in your coding agent and ask:

> Install the skills from this repository on this machine.

To bring existing personal skills into the repository, ask:

> Move my existing personal skills into this repository and link them.

The agent should follow [AGENTS.md](AGENTS.md) to discover skills, translate imported content into English when needed, preserve existing files, create individual symlinks, and verify the result. These actions run when requested; cloning alone does not install skills.

## Planning workflow

Use `$create-plan` to turn an agreed design or concrete request into plans under `docs/plans`. Each file contains exactly one implementation step, human-reviewable pseudo code, completion criteria, and a verification plan. Multiple steps use separate files connected by explicit dependency links.

Plan creation includes a required fresh-context agent review. Use `$implement-plan` to execute or resume a reviewed plan and record its results in that same file. A passing plan review does not mean the implementation has been completed or reviewed.

The [shared plan contract](create-plan/references/plan-contract.md) and [template](create-plan/assets/plan-template.md) are maintained in `create-plan` and consumed by `implement-plan`. Install `create-plan`, `implement-plan`, and `fresh-context-review` together.

`docs/designs` records design decisions, `docs/plans` records executable steps and their results, and `docs/todos` tracks deferred work. Link related documents without duplicating their status or treating a planning milestone as implementation completion.

## Sync changes

- Pull the latest changes before editing skills.
- Edit the files, then commit and push from this repository.
- Pull on other machines to update their linked skills.
- When adding a new skill, create its symlink on each machine where it should be available.

Git provides version history and sharing; synchronization still requires pushing and pulling. Keep bundled skills, caches, and machine-generated files such as `.DS_Store` out of version control.
