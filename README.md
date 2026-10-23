# .github

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENCE)

Organization-wide files for [Kionga](https://github.com/kiongahq): the public
profile page, the shared CI workflows every component uses, and the repository
list.

| Path | What it is |
| --- | --- |
| `profile/README.md` | The organization's GitHub profile page |
| `.github/workflows/go.yml` | Reusable Go checks: gofmt, vet, race tests and build, then govulncheck, gosec and gitleaks |
| `.github/workflows/python.yml` | Reusable Python checks: install, ruff and pytest, then pip-audit, bandit and gitleaks |
| `.github/workflows/image.yml` | Reusable image build; publishes `ghcr.io/kiongahq/<image>` from `main` and `v*` tags |
| `repos.txt` | Every Kionga repository, in dependency order |
| `roadmap/` | Improvement issue sources, by month |
| `migration/` | Record of how the repositories were split out of the original monorepo |

## Usage

Call a workflow from a component repository:

```yaml
jobs:
  go:
    uses: kiongahq/.github/.github/workflows/go.yml@main
  image:
    needs: go
    uses: kiongahq/.github/.github/workflows/image.yml@main
    permissions: {contents: read, packages: write}
    with: {image: serving-manager}
```

`python.yml` takes a required `install` command (for example
`pip install -r requirements-dev.txt`) and an optional `python-version` (default
`3.11`). `image.yml` takes `image` and optionally `context`, `dockerfile`,
`build-args` and `platforms`. Images are tagged `sha-<short>`, `latest` on the
default branch, and `X.Y.Z` and `X.Y` on semantic version tags; pull requests build
without publishing.

## Security gates

Both check workflows fail the build on a reachable vulnerability (govulncheck,
pip-audit), a medium-or-higher static finding (gosec, bandit) or a secret anywhere
in the Git history (gitleaks). Tool versions are pinned in the workflows. A reviewed
false positive is annotated where it occurs, with the reason:

- Go: `// #nosec G704 -- host is operator config` on the flagged line.
- Python: the reason in a comment on the line before, and `# nosec B104` at the end
  of the flagged line with nothing after it.

Fake credentials in tests go in the repository's `.gitleaksignore` by fingerprint,
so a new finding still fails.

## migration/

Each `*.manifest` lists the paths one repository took from the platform monorepo
(at commit `441621b`, which is `c69f52d` after a history rewrite that removed a
draft file), with their history, using
[`git-split-repo.sh`](https://github.com/Markkimotho/automation-scripts-utils).
`rewrite_docs_paths.py` converted monorepo paths in the docs to the new layout.
Both are kept as a record and are not part of any build.

## License

[MIT](LICENCE) © Kionga contributors
