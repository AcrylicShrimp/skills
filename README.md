# Personal Skills

This repository is intended to hold my personal Codex skills and keep them in sync across machines through Git. Each skill lives in its own directory, including its `SKILL.md` and any supporting scripts, references, or assets.

All imported skills must be in English. Non-English skills are translated during import while preserving their meaning and behavior. The detailed rules and agent procedures live in [AGENTS.md](AGENTS.md).

## Symlink layout

Keep the actual skill files in this repository and create a symbolic link for each skill directory inside the local Codex skills directory:

```text
~/Devel/skills/                    # Git working copy: actual files
├── README.md
├── AGENTS.md
├── baby-mode/
│   └── SKILL.md
└── create-todo/
    └── SKILL.md

~/.codex/skills/                   # Local Codex skills directory
├── .system/                       # Bundled skills, kept locally
├── baby-mode -> ~/Devel/skills/baby-mode
└── create-todo -> ~/Devel/skills/create-todo
```

This is the intended layout; the skill names are examples. Editing a file through either path changes the same file, and Git tracks changes in this repository.

The paths above match my current setup. The [official Codex documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) currently lists `~/.agents/skills` as the user skills location and confirms support for symlinked skill folders. Use the directory your Codex installation reads when setting up another machine.

## Why link individual skills?

Link each skill directory instead of replacing the entire local skills directory with one symlink. This keeps bundled `.system` skills and any machine-specific skills separate from the repository.

Linking the entire directory would make newly added skills available without creating additional links, but it would also place local contents such as `.system` in the repository's working directory. Individual links provide more control over which skills are shared and enabled on each machine.

## Set up a machine

1. Clone this repository, for example into `~/Devel/skills`.
2. Create the local skills directory if it does not exist.
3. Add a symlink for each skill you want to use.

For example, once `baby-mode` exists in the repository:

```sh
mkdir -p "$HOME/.codex/skills"
ln -s "$HOME/Devel/skills/baby-mode" "$HOME/.codex/skills/baby-mode"
```

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
