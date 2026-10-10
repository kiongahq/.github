# Roadmap issue sources

Each `<date>/<repo>.json` is the list of improvement issues filed in that
repository: `{title, body, labels}` with one type label, one priority
(`P1` security, data-loss or correctness risk; `P2`; `P3`) and one `area:` label.
Every issue cites the code it is about.

They were filed with
[`gh-issues-sync.py`](https://github.com/Markkimotho/automation-scripts-utils),
which creates missing labels and skips titles that already exist, so re-running
is safe:

```bash
gh-issues-sync.py roadmap/2026-10/serving.json -R kiongahq/serving          # preview
gh-issues-sync.py roadmap/2026-10/serving.json -R kiongahq/serving --apply
```

The issues on GitHub are the live record; these files are what was filed.
