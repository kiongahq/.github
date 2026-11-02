# Repository merge controls

The default branch, `main`, and `master` are release boundaries, including when these named branches are created later. All public repositories require pull requests, resolution of review conversations, and successful required checks against an up-to-date base. While the organization has one maintainer, approval counts are zero and mandatory code-owner, latest-push, and unattributed-change approvals are disabled. Optional approvals are dismissed after new commits. Administrators and automation have no bypass entry. Deletion and force-pushing are blocked for these branches and `v*` release tags.

A maintainer cannot approve their own pull request. The sole maintainer reviews the diff, resolves comments, waits for required checks, and merges the pull request without a separate approving review. This also means no human approval is enforced for other authors; grant write access deliberately. When another trusted maintainer joins, update CODEOWNERS and enable independent review with the script option below. Do not disable test or security gates to merge changes. Organization owners can still change repository settings; repository rules cannot defend against a compromised owner account. Use strong MFA, preferably hardware-backed passkeys, and narrowly scoped GitHub App credentials.

## Required verification

- Existing component tests, formatting, lint, type checks, builds, and integration checks remain required. Post-merge publishing and scheduled load tests are not PR gates.
- Repository guardrails validate workflow syntax and shell commands, require immutable external action and reusable-workflow references, and scan full Git history for secrets with redacted output.
- Public PRs undergo dependency review, blocking newly introduced vulnerabilities of moderate severity or higher.
- CodeQL uses the extended query suite. Merge protection blocks security alerts of medium severity or higher and code-quality errors; missing or incomplete analysis also blocks merging.
- Dependabot checks supported manifests and Actions weekly. Security-update PRs require the same review and checks as other changes; they are not automatically merged.

Checks are bound to the GitHub Actions application. Keep CODEOWNERS to identify ownership and support future independent review. The maintainer must inspect workflow files, CODEOWNERS, and scanner exclusions carefully: status-check names alone cannot prove that an untrusted workflow ran the intended checks. Organization-level required workflows provide stronger central enforcement where the GitHub plan supports them.

## CI trust boundaries

Every external contributor requires workflow approval, including returning contributors. Inspect changes to workflows, actions, dependency installation, build scripts, and test hooks before granting approval. Approval authorizes code execution; it is not a code review or merge approval.

Default workflow tokens are read-only and cannot approve pull requests. Checkout credentials are not persisted. PR image builds have read-only tokens. Image publication runs only on default-branch or release-tag events, and release tags must reference commits contained in the default branch. Publishing jobs receive only the additional permissions they need. Never run untrusted PR code using `pull_request_target`, repository secrets, or persistent self-hosted runners.

Secret scanning, push protection, private vulnerability reporting, Dependabot alerts, and security updates are enabled on public repositories. If a real credential is detected, revoke it first; deleting the text does not invalidate the credential. Scanner exclusions require a narrow fingerprint or rule, an explanation, and review. Do not silence a finding simply to make a check green.

## Administration and onboarding

`python3 security/repository_rules.py REPOSITORY` prints the intended rules. Add `--apply` to create or reconcile only the named managed rulesets. Install and verify the workflows and CodeQL first. Applying a required check that never runs intentionally blocks merges.

The default configuration supports a sole maintainer. Once another trusted reviewer is available, use `python3 security/repository_rules.py REPOSITORY --require-independent-review --apply` to require one fresh approval, code-owner review, and independent approval of the latest push. Continue passing that option on subsequent reconciliations while independent review is required.

Before adding a repository, configure CODEOWNERS, the shared guardrails workflow at a reviewed commit SHA, the component-specific CI checks, Dependabot, CodeQL, secret protection, read-only workflow permissions, and approval for all external contributors. Add its exact PR check names to the script and apply the rules. Verify the saved configuration and effective rules for both `main` and `master` through GitHub after each change. If using `master`, ensure all required checks and code scanning run for pull requests targeting it; missing checks must block merging.

The November 2026 rollout covers the 11 public repositories. The private `demo-repository` receives CI configuration and supported dependency/token settings, but GitHub Free does not enforce private-repository branch rules. GitHub Team is needed for private branch protection and organization-level rules. Private code/secret scanning can require separate GitHub security entitlements. Do not make private code public to gain protections.

Organization-wide defaults and policies require an administrator token with the appropriate organization permissions (`admin:org` for a classic token). Until these are configured, new repositories require the onboarding steps above. No access token belongs in this repository or in command output.

These controls reduce risk; they cannot guarantee that code is free of vulnerabilities. Reviewers must examine authorization, tenant boundaries, input validation, dependency provenance, and operational impact, supported by meaningful regression tests.
