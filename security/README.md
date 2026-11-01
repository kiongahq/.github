# Repository merge controls

The default branch is a release boundary. All public repositories require pull requests, one fresh approving review, code-owner approval, resolution of review conversations, and successful required checks against an up-to-date base. Approvals are dismissed after new commits; the latest reviewable push must be approved by another person. Administrators and automation have no bypass entry. Deletion and force-pushing are blocked for the default branch, `main`, and `v*` release tags.

A maintainer cannot approve their own pull request. With only one maintainer, add another trusted reviewer with write access and update CODEOWNERS before expecting maintainer-authored changes to merge. Do not temporarily weaken rules to merge routine changes. Organization owners can still change repository settings; repository rules cannot defend against a compromised owner account. Use strong MFA, preferably hardware-backed passkeys, and narrowly scoped GitHub App credentials.

## Required verification

- Existing component tests, formatting, lint, type checks, builds, and integration checks remain required. Post-merge publishing and scheduled load tests are not PR gates.
- Repository guardrails validate workflow syntax and shell commands, require immutable external action and reusable-workflow references, and scan full Git history for secrets with redacted output.
- Public PRs undergo dependency review, blocking newly introduced vulnerabilities of moderate severity or higher.
- CodeQL uses the extended query suite. Merge protection blocks security alerts of medium severity or higher and code-quality errors; missing or incomplete analysis also blocks merging.
- Dependabot checks supported manifests and Actions weekly. Security-update PRs require the same review and checks as other changes; they are not automatically merged.

Checks are bound to the GitHub Actions application. Workflow files, CODEOWNERS, and scanner exclusions require code-owner review. Review these changes carefully: status-check names alone cannot prove that an untrusted workflow ran the intended checks. Organization-level required workflows provide stronger central enforcement where the GitHub plan supports them.

## CI trust boundaries

Every external contributor requires workflow approval, including returning contributors. Inspect changes to workflows, actions, dependency installation, build scripts, and test hooks before granting approval. Approval authorizes code execution; it is not a code review or merge approval.

Default workflow tokens are read-only and cannot approve pull requests. Checkout credentials are not persisted. PR image builds have read-only tokens. Image publication runs only on default-branch or release-tag events, and release tags must reference commits contained in the default branch. Publishing jobs receive only the additional permissions they need. Never run untrusted PR code using `pull_request_target`, repository secrets, or persistent self-hosted runners.

Secret scanning, push protection, private vulnerability reporting, Dependabot alerts, and security updates are enabled on public repositories. If a real credential is detected, revoke it first; deleting the text does not invalidate the credential. Scanner exclusions require a narrow fingerprint or rule, an explanation, and review. Do not silence a finding simply to make a check green.

## Administration and onboarding

`python3 security/repository_rules.py REPOSITORY` prints the intended rules. Add `--apply` to create or reconcile only the named managed rulesets. Install and verify the workflows and CodeQL first. Applying a required check that never runs intentionally blocks merges.

Before adding a repository, configure CODEOWNERS, the shared guardrails workflow at a reviewed commit SHA, the component-specific CI checks, Dependabot, CodeQL, secret protection, read-only workflow permissions, and approval for all external contributors. Add its exact PR check names to the script and apply the rules. Verify the saved configuration through GitHub after each change.

The November 2026 rollout covers the 11 public repositories. The private `demo-repository` receives CI configuration and supported dependency/token settings, but GitHub Free does not enforce private-repository branch rules. GitHub Team is needed for private branch protection and organization-level rules. Private code/secret scanning can require separate GitHub security entitlements. Do not make private code public to gain protections.

Organization-wide defaults and policies require an administrator token with the appropriate organization permissions (`admin:org` for a classic token). Until these are configured, new repositories require the onboarding steps above. No access token belongs in this repository or in command output.

These controls reduce risk; they cannot guarantee that code is free of vulnerabilities. Reviewers must examine authorization, tenant boundaries, input validation, dependency provenance, and operational impact, supported by meaningful regression tests.
