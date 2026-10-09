#!/usr/bin/env python3
"""Rewrite monorepo paths and make targets in the docs to the multi-repo layout.

Convention after the split: paths in the docs are relative to the workspace
directory that holds every checkout (KIONGA_SRC), e.g. deploy/compose.yaml,
platform/go/..., sdk-python/mlaiops_sdk/.... Commands run from there too:
`make -C deploy local-up`.

Usage: rewrite_docs_paths.py <docs-dir>   (prints per-rule counts; edits in place)
"""
import re
import sys
from collections import Counter
from pathlib import Path

# (monorepo prefix, workspace path), most specific first. A prefix only matches
# at a path boundary, so `deploy/x` inside `platform/deploy/x` is untouched.
PATHS = [
    ("deploy/jupyter/", "workspace/jupyter/"),
    ("deploy/ide/", "workspace/ide/"),
    ("deploy/workspace/", "workspace/workspace/"),
    ("scripts/vendor-manifest.py", "platform/scripts/vendor-manifest.py"),
    ("scripts/integration-test.sh", "platform/scripts/integration-test.sh"),
    ("scripts/", "deploy/scripts/"),
    ("config/", "deploy/config/"),
    ("tests/ui/", "platform/tests/ui/"),
    ("tests/e2e/", "platform/tests/e2e/"),
    ("tests/load/", "deploy/tests/load/"),
    ("go/cmd/serving-manager", "serving/cmd/serving-manager"),
    ("go/internal/serving", "serving/internal/serving"),
    ("go/cmd/trace-proxy", "trace-proxy/cmd/trace-proxy"),
    ("go/internal/traceproxy", "trace-proxy/internal/traceproxy"),
    ("go/", "platform/go/"),
    ("python/tests/test_workspace_directories.py", "workspace/tests/test_workspace_directories.py"),
    ("python/tests/test_feature_store_correctness.py", "agent-runtime/tests/test_feature_store_correctness.py"),
    ("python/mlaiops_sdk", "sdk-python/mlaiops_sdk"),
    ("python/pyproject.toml", "sdk-python/pyproject.toml"),
    ("python/agent_runtime/Dockerfile", "agent-runtime/Dockerfile"),
    ("python/agent_runtime", "agent-runtime/agent_runtime"),
    ("python/agents", "agent-runtime/agents"),
    ("python/features", "agent-runtime/features"),
    ("python/realtime", "agent-runtime/realtime"),
    ("python/pipelines/Dockerfile", "pipeline-runner/Dockerfile"),
    ("python/pipelines", "pipeline-runner/pipelines"),
]

MAKE = {
    "deploy": ["local-up", "local-rebuild", "local-status", "local-logs", "local-down", "local",
               "ide-up", "ide-down", "ide-agents-up", "public-up", "public-down", "kind-up",
               "test-load", "test-stress"],
    "platform": ["verify", "test-integration", "build", "test-ui", "test-go", "run", "test-browser",
                 "install", "test"],
    "docs": ["docs-build", "docs-serve", "docs-install"],
}
RENAMED_TARGETS = {"test-e2e": ("deploy", "test-e2e-kind")}


def rewrite(text: str, counts: Counter) -> str:
    for old, new in PATHS:
        pattern = re.compile(r"(?<![\w./-])" + re.escape(old))
        text, n = pattern.subn(new, text)
        counts[f"{old} -> {new}"] += n
    for repo, targets in MAKE.items():
        for target in targets:
            pattern = re.compile(r"(?<![\w-])make " + re.escape(target) + r"(?![\w-])")
            text, n = pattern.subn(f"make -C {repo} {target}", text)
            counts[f"make {target} -> make -C {repo}"] += n
    for target, (repo, new) in RENAMED_TARGETS.items():
        pattern = re.compile(r"(?<![\w-])make " + re.escape(target) + r"(?![\w-])")
        text, n = pattern.subn(f"make -C {repo} {new}", text)
        counts[f"make {target} -> make -C {repo} {new}"] += n
    return text


def main(root: str) -> int:
    counts: Counter = Counter()
    for path in sorted(Path(root).rglob("*.md")):
        before = path.read_text()
        after = rewrite(before, counts)
        if after != before:
            path.write_text(after)
    for rule, n in sorted(counts.items()):
        if n:
            print(f"{n:4}  {rule}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
