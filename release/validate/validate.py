"""Validate release versions before any package is published."""
import json
import os
from pathlib import Path
import re
import subprocess
import tomllib

VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")


def validate(root, tag="", branch="main"):
    version = (root / "version.txt").read_text().strip()
    if not VERSION.fullmatch(version):
        raise ValueError("version.txt must be a numeric X.Y.Z version")
    manifest = json.loads((root / ".release-please-manifest.json").read_text())
    if manifest != {".": version}:
        raise ValueError("release manifest and version.txt must agree")
    config = json.loads((root / "release-please-config.json").read_text())
    package = config["packages"]["."]
    if package.get("include-component-in-tag") is not False:
        raise ValueError("release tags must use vX.Y.Z without a component prefix")
    if package.get("version-file") != "version.txt":
        raise ValueError("release automation must update version.txt")
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        project = tomllib.loads(pyproject.read_text()).get("project", {})
        if "version" in project and project["version"] != version:
            raise ValueError("Python package version must match the release version")
    chart = root / "helm/kionga/Chart.yaml"
    if chart.exists():
        match = re.search(r"^version:\s*[\"']?([0-9.]+)[\"']?\s*$", chart.read_text(), re.MULTILINE)
        if not match or match[1] != version:
            raise ValueError("Helm chart version must match the deploy release")
    if not tag:
        return version
    if tag != "v" + version or version == "0.0.0":
        raise ValueError("release tag must match the nonzero version in the reviewed source")
    changelog = (root / "CHANGELOG.md").read_text()
    if not re.search(r"^## \[?" + re.escape(version) + r"(?:\]|\s|$)", changelog, re.MULTILINE):
        raise ValueError("release version must have a changelog entry")
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
    if git("rev-parse", "HEAD") != git("rev-parse", "refs/tags/" + tag + "^{commit}"):
        raise ValueError("checkout must match the release tag")
    subprocess.run(["git", "merge-base", "--is-ancestor", "HEAD", "refs/remotes/origin/" + branch],
                   cwd=root, check=True)
    return version


if __name__ == "__main__":
    version = validate(Path.cwd(), os.environ.get("RELEASE_TAG", ""),
                       os.environ.get("DEFAULT_BRANCH", "main"))
    print(f"Validated release metadata: {version}")
