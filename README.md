# .github

Organization-wide files for [Kionga](https://github.com/kiongahq).

| Path | Purpose |
| --- | --- |
| `profile/README.md` | The organization's GitHub profile page |
| `.github/workflows/go.yml` | Reusable Go checks: gofmt, vet, race tests, build, then govulncheck, gosec and gitleaks |
| `.github/workflows/python.yml` | Reusable Python checks: install, ruff, pytest, then pip-audit, bandit and gitleaks |
| `.github/workflows/image.yml` | Reusable image build; publishes `ghcr.io/kiongahq/<image>` from `main` and `v*` tags |
| `repos.txt` | Every Kionga repository, in dependency order |
| `migration/` | How the repositories were split out of the original monorepo |

Use a workflow from a component repository:

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

## Security gates

Both reusable workflows fail the build on a reachable vulnerability (govulncheck,
pip-audit), a medium-or-higher static finding (gosec, bandit) or a secret anywhere
in the history (gitleaks). Tool versions are pinned in the workflows. A reviewed
false positive is annotated where it occurs, with the reason:
`// #nosec G704 -- host is operator config` in Go, and in Python a comment line
with the reason above the flagged line, which ends in `# nosec B104`. Fake credentials in tests go in the repository's
`.gitleaksignore` by fingerprint, so a new finding still fails.

## migration/

Each `*.manifest` lists the paths one repository took from the platform monorepo
(at commit `441621b`, which is `c69f52d` after the history rewrite that removed a draft file), with their history, using
[`git-split-repo.sh`](https://github.com/Markkimotho/automation-scripts-utils):

```bash
git-split-repo.sh ~/mlops ~/kionga/serving -b main -m migration/serving.manifest
```

`rewrite_docs_paths.py` converted monorepo paths in the docs to the workspace
layout. Both are kept as a record; they are not part of any build.
