# .github

Organization-wide files for [Kionga](https://github.com/kiongahq).

| Path | Purpose |
| --- | --- |
| `profile/README.md` | The organization's GitHub profile page |
| `.github/workflows/go.yml` | Reusable Go checks: gofmt, vet, race tests, build |
| `.github/workflows/python.yml` | Reusable Python checks: install, ruff, pytest |
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

## migration/

Each `*.manifest` lists the paths one repository took from the platform monorepo
(at commit `441621b`), with their history, using
[`git-split-repo.sh`](https://github.com/Markkimotho/automation-scripts-utils):

```bash
git-split-repo.sh ~/mlops ~/kionga/serving -b main -m migration/serving.manifest
```

`rewrite_docs_paths.py` converted monorepo paths in the docs to the workspace
layout. Both are kept as a record; they are not part of any build.
