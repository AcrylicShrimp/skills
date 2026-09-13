# Repository Instructions

These instructions apply throughout this repository. Keep repository documentation in English. See [README.md](README.md) for the repository purpose and symlink layout.

## Language requirement

Skills imported into this repository must be in English. Translate any non-English instructions and explanatory prose before completing the import, including `SKILL.md`, descriptive metadata, supporting documentation, templates, and code comments. This translation is a required part of migration and does not need a separate request.

Preserve the original meaning, requirements, constraints, and behavior. Keep functional identifiers, commands, paths, URLs, and literal examples or test data unchanged where translation would change their meaning or break functionality. Writing a skill in English does not change any explicit requirement about the language of its output.

Keep an untouched backup of the original skill outside the repository. Review the translated version for completeness and semantic equivalence before linking it into the local skills directory.

## Skill installation and migration

When asked to install this repository's skills or move existing personal skills into this repository, follow this file and perform the requested setup. The request authorizes the corresponding file operations below; do not stop at providing commands or ask for routine confirmation. This is an agent-executed workflow, not a hook that runs automatically on clone.

Use the actual checkout path rather than assuming `~/Devel/skills`. Determine the active local skills directory from the current installation and available session context. In the setup documented here, it is `~/.codex/skills`; other installations may use `~/.agents/skills`. Do not install the same skills into both locations by default.

### Install skills from a cloned repository

For requests such as “Install the skills from this repository on this machine”:

1. Discover the repository's immediate child directories that contain a `SKILL.md`. Install all of them unless the user names a subset. Ignore hidden directories, including `.git` and `.system`.
2. Create the active local skills directory if needed. Keep its `.system` directory and unrelated local skills in place.
3. For each selected skill, create a symlink from the local skills directory to the actual skill directory in this checkout. Use an absolute target path.
4. If the destination is already a symlink resolving to that directory, leave it as is. Repeated setup must be safe.
5. If the destination is an existing directory, file, or a different symlink, move that entry into a uniquely named backup directory outside the active skills directory before creating the new link. Preserve the entry as-is; do not delete it or silently merge its contents. Record its original and backup paths.
6. Verify that every installed link resolves to its intended repository directory and that `SKILL.md` is readable through the link. Report the installed skills, any unchanged links, and any backups. If there are no skill directories in the checkout, report that instead of inventing or downloading skills.

### Move existing personal skills into this repository

For requests such as “Move my existing personal skills into this repository and link them”:

1. Discover immediate child directories containing `SKILL.md` in the active local skills directory. Honor any user-specified subset. Exclude hidden directories and bundled `.system` skills.
2. For each ordinary skill directory absent from the repository, copy its complete contents into a same-named repository directory, preserving supporting files, executable permissions, and internal symlinks. Verify the initial copy against the source, then apply the language requirement above to the repository copy. Do not modify the original through an internal symlink. Review all translation changes and verify that functional content remains intact before replacing the local directory with a link using the backup procedure above; retain the untouched original in that backup.
3. If a same-named repository directory already exists, compare the complete directories. If they match, apply the language requirement before linking and preserve the local original in a backup. If they differ, preserve both versions and ask which should become the shared version; continue processing other non-conflicting skills in the meantime. Apply the language requirement to the selected version before completing its import.
4. Leave links already pointing into this checkout unchanged. Do not import the contents of links pointing elsewhere automatically; report them separately because their source may be managed by another repository or installation.
5. Ensure the repository's `.gitignore` excludes `.system/`, `.DS_Store`, `__pycache__/`, and `*.pyc`, preserving any existing ignore rules. Translate non-English skill content as required above; otherwise preserve the skill's meaning and behavior without unrelated rewrites.
6. Verify the English content and final links, and report the imported skills, translated files, backup locations, and any unresolved conflicts. Do not claim that Git history or remote synchronization is configured unless it actually is. Creating a remote repository, committing, and pushing require a request that includes those actions.

Complete the requested file setup and verification directly. Ask for clarification only when the active skills location cannot be determined or when conflicting content requires a choice. File and link verification confirms the filesystem setup; claim successful Codex discovery only if it was also observed.
