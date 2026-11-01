import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("validate", Path(__file__).parents[1] / "validate/validate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReleaseValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "version.txt").write_text("1.2.3\n")
        (self.root / ".release-please-manifest.json").write_text('{".": "1.2.3"}')
        (self.root / "release-please-config.json").write_text(json.dumps({"packages": {".": {
            "version-file": "version.txt", "include-component-in-tag": False}}}))
        (self.root / "CHANGELOG.md").write_text("# Changelog\n\n## 1.2.3\n\nFixes.\n")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.DEVNULL, text=True).strip()

    def repository(self):
        self.git("init", "-b", "main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.git("add", ".")
        self.git("commit", "-m", "release")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("tag", "v1.2.3")

    def test_reviewed_release(self):
        self.repository()
        self.assertEqual(module.validate(self.root, "v1.2.3"), "1.2.3")

    def test_rejects_unreviewed_commit(self):
        self.repository()
        self.git("commit", "--allow-empty", "-m", "unreviewed")
        self.git("tag", "-f", "v1.2.3")
        with self.assertRaises(subprocess.CalledProcessError):
            module.validate(self.root, "v1.2.3")

    def test_tag_cannot_select_different_commit(self):
        self.repository()
        self.git("commit", "--allow-empty", "-m", "later")
        with self.assertRaisesRegex(ValueError, "checkout"):
            module.validate(self.root, "v1.2.3")

    def test_rejects_mismatched_tag_and_missing_notes(self):
        with self.assertRaisesRegex(ValueError, "tag"):
            module.validate(self.root, "v9.0.0")
        (self.root / "CHANGELOG.md").write_text("# Changelog\n")
        with self.assertRaisesRegex(ValueError, "changelog"):
            module.validate(self.root, "v1.2.3")

    def test_rejects_version_drift(self):
        (self.root / "pyproject.toml").write_text('[project]\nversion = "1.2.2"\n')
        with self.assertRaisesRegex(ValueError, "Python"):
            module.validate(self.root)
        (self.root / "pyproject.toml").unlink()
        (self.root / ".release-please-manifest.json").write_text('{".": "1.2.2"}')
        with self.assertRaisesRegex(ValueError, "manifest"):
            module.validate(self.root)

    def test_rejects_invalid_version(self):
        for version in ("01.2.3", "v1.2.3", "1.2", "$(id)", "1.2.3-rc.1"):
            (self.root / "version.txt").write_text(version)
            with self.assertRaises(ValueError):
                module.validate(self.root)


if __name__ == "__main__":
    unittest.main()
