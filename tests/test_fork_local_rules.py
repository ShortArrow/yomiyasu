"""Keep the fork's hook into references/local/ through upstream merges.

The shortarrow branch adds one paragraph to SKILL.md that makes the skill read references/local/. Upstream rewrites
SKILL.md freely (3.0.0 rewrote most of it), so a merge can drop or move that paragraph without any conflict marker.
references/local/README.md says where the paragraph belongs: right before the Step 2 heading.
"""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "yomiyasu" / "SKILL.md"
PARAGRAPH_START = "**独自の規則**: `references/local/` に `.md` のファイルがあれば"
STEP2_HEADING = "### Step 2:"


class ForkLocalRulesTests(unittest.TestCase):
    def test_paragraph_appears_once_right_before_step2(self):
        lines = SKILL.read_text(encoding="utf-8").splitlines()
        starts = [index for index, line in enumerate(lines) if line.startswith(PARAGRAPH_START)]
        self.assertEqual(len(starts), 1, "SKILL.md must carry the references/local/ paragraph exactly once")
        following = [line for line in lines[starts[0] + 1:] if line.strip()]
        self.assertTrue(following and following[0].startswith(STEP2_HEADING),
                        "the references/local/ paragraph must sit right before the Step 2 heading")

    def test_local_folder_has_rules_besides_readme(self):
        rules = sorted(path.name for path in (ROOT / "references" / "local").glob("*.md") if path.name != "README.md")
        self.assertTrue(rules, "references/local/ holds no rule files")


if __name__ == "__main__":
    unittest.main()
