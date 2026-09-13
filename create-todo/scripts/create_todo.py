#!/usr/bin/env python3
import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

STATUS_VALUES = {
    "not-started": "Not Yet Started",
    "in-progress": "Partially Taken",
    "completed": "Finished",
    "dropped": "Dropped",
}

LOG_CATEGORIES = ("USER", "ACTION", "RESULT")


def slugify(raw: str) -> str:
    value = raw.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    if not value:
        return "todo-item"
    return value


def next_counter_for_date(docs_dir: Path, date_prefix: str) -> int:
    pattern = re.compile(rf"^{re.escape(date_prefix)}\.(\d{{2}})\..+\.md$")
    counters = []
    if docs_dir.exists():
        for entry in docs_dir.iterdir():
            if not entry.is_file():
                continue
            match = pattern.match(entry.name)
            if match:
                counters.append(int(match.group(1)))

    if not counters:
        return 0

    next_value = max(counters) + 1
    if next_value > 99:
        raise ValueError(
            f"counter overflow for {date_prefix}: max supported counter is 99"
        )
    return next_value


def default_docs_dir() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        repo_root = result.stdout.strip()
        if repo_root:
            return Path(repo_root) / "docs" / "todos"
    except Exception:
        pass

    return Path.cwd() / "docs" / "todos"


def format_log_line(timestamp: str, category: str, detail: str) -> str:
    detail = " ".join(detail.strip().split())
    return f"- [{timestamp}] [{category}] {detail}"


def build_content(
    *,
    title: str,
    status_key: str,
    dropped_reason: str,
    updated_at: str,
    context: str,
    why_needed: str,
    completion_criteria: str,
    detailed_plan: str,
    pseudo_code_diff: str,
    user_note: str,
    action_note: str,
    result_note: str,
) -> str:
    status_text = STATUS_VALUES[status_key]
    dropped_line = dropped_reason if status_key == "dropped" else ""

    log_lines = [
        format_log_line(updated_at, "USER", user_note),
        format_log_line(updated_at, "ACTION", action_note),
        format_log_line(updated_at, "RESULT", result_note),
    ]

    return f"""# TODO: {title}

## Current Status
- State: {status_text}
- Dropped Reason: {dropped_line}
- Last Status Update: {updated_at}

## Context
{context}

## Why It Is Needed
{why_needed}

## Completion Criteria
{completion_criteria}

## Detailed Plan
{detailed_plan}

## Pseudo Code Diff
{pseudo_code_diff}

## Activity Log
{os.linesep.join(log_lines)}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a TODO markdown file at docs/YYYY-MM-DD.NN.name-of-the-task.md "
            "with standardized sections and activity log entries."
        )
    )
    parser.add_argument("title", help="Task title used for heading and filename slug")
    parser.add_argument(
        "--docs-dir",
        default=None,
        help=(
            "Target docs directory. Default is repository-root/docs/todos "
            "(falls back to current-working-directory/docs/todos outside a git repo)."
        ),
    )
    parser.add_argument(
        "--status",
        default="not-started",
        choices=tuple(STATUS_VALUES.keys()),
        help="Initial task status",
    )
    parser.add_argument(
        "--dropped-reason",
        default="",
        help="Reason when status is dropped",
    )
    parser.add_argument(
        "--context",
        default="",
        help="Context section content",
    )
    parser.add_argument(
        "--why-needed",
        default="",
        help="Justification/evidence section content",
    )
    parser.add_argument(
        "--completion-criteria",
        default="",
        help="Completion criteria section content",
    )
    parser.add_argument(
        "--detailed-plan",
        default="",
        help="Detailed plan section content",
    )
    parser.add_argument(
        "--pseudo-code-diff",
        default="",
        help=(
            "Pseudo Code Diff section content. Required by policy for TODOs that "
            "include code changes; use 'Not applicable.' for non-code TODOs."
        ),
    )
    parser.add_argument(
        "--user-note",
        default="",
        help="USER category activity log detail",
    )
    parser.add_argument(
        "--action-note",
        default="",
        help="ACTION category activity log detail",
    )
    parser.add_argument(
        "--result-note",
        default="",
        help="RESULT category activity log detail",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    now = dt.datetime.now().replace(microsecond=0)
    date_prefix = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    docs_dir = Path(args.docs_dir) if args.docs_dir else default_docs_dir()
    docs_dir.mkdir(parents=True, exist_ok=True)

    slug = slugify(args.title)

    try:
        counter = next_counter_for_date(docs_dir, date_prefix)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    filename = f"{date_prefix}.{counter:02d}.{slug}.md"
    target_path = docs_dir / filename

    if target_path.exists():
        print(f"target file already exists: {target_path}", file=sys.stderr)
        return 1

    if args.status == "dropped" and not args.dropped_reason.strip():
        print("--dropped-reason is required when --status=dropped", file=sys.stderr)
        return 1

    context = args.context.strip() or ""
    why_needed = args.why_needed.strip() or ""
    completion_criteria = args.completion_criteria.strip() or ""
    detailed_plan = args.detailed_plan.strip() or ""
    pseudo_code_diff = args.pseudo_code_diff.strip() or "Not applicable."

    user_note = args.user_note.strip() or f"Created from request: {args.title.strip()}"
    action_note = (
        args.action_note.strip()
        or f"Created TODO file using create_todo.py with status={args.status}"
    )
    result_note = args.result_note.strip() or f"TODO file created at {target_path}"

    content = build_content(
        title=args.title.strip(),
        status_key=args.status,
        dropped_reason=args.dropped_reason.strip(),
        updated_at=timestamp,
        context=context,
        why_needed=why_needed,
        completion_criteria=completion_criteria,
        detailed_plan=detailed_plan,
        pseudo_code_diff=pseudo_code_diff,
        user_note=user_note,
        action_note=action_note,
        result_note=result_note,
    )

    target_path.write_text(content, encoding="utf-8")
    print(target_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
