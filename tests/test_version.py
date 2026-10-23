import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def project_version() -> str:
    content = (ROOT / "pyproject.toml").read_text()
    match = re.search(r'^version = "([^"]+)"$', content, re.MULTILINE)
    assert match, "version not found in pyproject.toml"
    return match.group(1)


def as_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def latest_tag_version() -> str | None:
    try:
        output = subprocess.check_output(
            ["git", "tag", "--list", "v*"], cwd=ROOT, text=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    versions = [
        tag[1:] for tag in output.split() if VERSION_RE.match(tag[1:])
    ]
    if not versions:
        return None
    return max(versions, key=as_tuple)


class TestVersion(unittest.TestCase):
    def test_version_format(self):
        self.assertRegex(project_version(), VERSION_RE)

    def test_version_bumped_since_latest_tag(self):
        latest = latest_tag_version()
        if latest is None:
            self.skipTest("no vX.Y.Z git tag available")
        self.assertGreater(
            as_tuple(project_version()),
            as_tuple(latest),
            f"pyproject.toml version must be bumped above the latest tag v{latest}",
        )
