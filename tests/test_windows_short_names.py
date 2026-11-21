"""On Windows, an 8.3 short name (SECRET~1 for .secret) does not start with a dot. The input path guard must still
refuse it, because it compares the real path, which os.path.realpath returns with the long names.

If the guard compared os.path.abspath instead, SECRET~1/key.md would pass the dot check and lint would print
the file. Skipped outside Windows and on volumes with 8.3 names turned off. Files live only in a temporary folder.
"""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import markdown_visibility  # noqa: E402

LINT = SCRIPTS / "yomiyasu_lint.py"
HIDDEN = markdown_visibility.INPUT_PATH_HIDDEN
SECRET_WORD = "青い鳥"


def _short_name(path: Path) -> str:
    """The 8.3 short form of an existing path, or the path unchanged when the volume has none."""
    import ctypes
    from ctypes import wintypes

    get_short = ctypes.windll.kernel32.GetShortPathNameW
    get_short.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    get_short.restype = wintypes.DWORD
    buffer = ctypes.create_unicode_buffer(1024)
    length = get_short(str(path), buffer, len(buffer))
    return buffer.value if 0 < length < len(buffer) else str(path)


@unittest.skipUnless(os.name == "nt", "8.3 short names exist only on Windows")
class ShortNameGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(os.path.realpath(self.temporary.name))
        (self.work / ".secret").mkdir()
        (self.work / ".secret" / "key.md").write_text("秘密の合言葉は青い鳥です。\n", encoding="utf-8")
        (self.work / ".envfile.md").write_text("秘密の合言葉は青い鳥です。\n", encoding="utf-8")
        current = os.getcwd()
        os.chdir(str(self.work))
        self.addCleanup(os.chdir, current)

    def _short_relative(self, relative: str) -> str:
        short = Path(_short_name(self.work / relative)).name
        if short.startswith("."):
            self.skipTest("this volume has no 8.3 short names")
        return short

    def test_short_name_of_a_dot_folder_is_refused(self):
        path = str(Path(self._short_relative(".secret")) / "key.md")
        self.assertEqual(markdown_visibility.input_path_problem(path), HIDDEN)

    def test_short_name_of_a_dot_file_is_refused(self):
        path = self._short_relative(".envfile.md")
        self.assertEqual(markdown_visibility.input_path_problem(path), HIDDEN)

    def test_lint_stops_without_printing_the_file(self):
        path = str(Path(self._short_relative(".secret")) / "key.md")
        environment = dict(os.environ, PYTHONUTF8="1")
        result = subprocess.run([sys.executable, str(LINT), path], capture_output=True, cwd=str(self.work),
                                env=environment, timeout=60)
        self.assertEqual(result.returncode, 2)
        output = (result.stdout + result.stderr).decode("utf-8", "replace")
        self.assertNotIn(SECRET_WORD, output)
        self.assertIn(HIDDEN, output)


if __name__ == "__main__":
    unittest.main()
