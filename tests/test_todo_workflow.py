import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CREATE = REPO / "create-todo/scripts/create_todo.py"
UPDATE = REPO / "update-todo/scripts/update_todo.py"


class TodoWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.docs = Path(self.workspace.name) / "docs/todos"

    def run_script(self, script, *args):
        return subprocess.run(
            [sys.executable, str(script), *args],
            capture_output=True,
            text=True,
            check=True,
        )

    def create_todo(self, pseudo_diff):
        result = self.run_script(
            CREATE,
            "Preserve the implementation contract",
            "--docs-dir", str(self.docs),
            "--pseudo-code-diff", pseudo_diff,
            "--completion-criteria", "- [ ] Existing contracts remain intact",
        )
        return Path(result.stdout.strip())

    def test_status_update_preserves_diff_extra_sections_and_existing_logs(self):
        pseudo_diff = "```diff\n+ fn validate_input() -> ValidatedInput;\n```"
        target = self.create_todo(pseudo_diff)
        original = target.read_text()
        original_logs = original.split("## Activity Log\n", 1)[1].strip()
        original = original.replace(
            "## Activity Log\n",
            "## Related Design\n../designs/input-contract.md\n\n## Activity Log\n",
        )
        target.write_text(original)

        self.run_script(UPDATE, "--file", str(target), "--status", "in-progress")

        updated = target.read_text()
        self.assertIn("- State: Partially Taken", updated)
        self.assertIn(original_logs, updated)
        # All content between status and logs survives the CLI round trip.
        original_body = original.split("## Context\n", 1)[1].split("## Activity Log\n", 1)[0]
        updated_body = updated.split("## Context\n", 1)[1].split("## Activity Log\n", 1)[0]
        self.assertEqual(updated_body, original_body)

    def test_explicit_diff_update_preserves_other_content(self):
        target = self.create_todo("```diff\n+ fn old_contract();\n```")
        replacement = "```diff\n+ fn new_contract() -> Result<()>;\n```"
        self.run_script(
            UPDATE, "--file", str(target), "--pseudo-code-diff", replacement,
        )
        updated = target.read_text()
        self.assertIn(replacement, updated)
        self.assertNotIn("fn old_contract", updated)
        self.assertIn("- State: Not Yet Started", updated)
        self.assertIn("- [ ] Existing contracts remain intact", updated)

    def test_fenced_headings_remain_part_of_the_diff(self):
        for fence in ("```", "~~~~"):
            with self.subTest(fence=fence):
                pseudo_diff = (
                    f"{fence}markdown\n## Context\nAn embedded heading.\n"
                    f"## Activity Log\nAn embedded log example.\n{fence}"
                )
                target = self.create_todo(pseudo_diff)
                self.run_script(UPDATE, "--file", str(target), "--status", "in-progress")
                self.assertIn(pseudo_diff, target.read_text())


if __name__ == "__main__":
    unittest.main()
