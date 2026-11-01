# Security policy

Report suspected vulnerabilities through the affected repository’s **Security → Report a vulnerability** page. Do not disclose exploit details, credentials, or private customer data in a public issue. Include affected versions, reproduction steps, impact, and a minimal proof of concept when available.

Security fixes target the current default branch. The platform is under active development; deployment operators should keep dependencies and container images updated and review release notes before upgrades.

Changes to authentication, authorization, tenant isolation, credential handling, workflow permissions, dependency sources, or deployment boundaries require focused security review and regression tests. Never add real secrets to source, test fixtures, logs, or pull request descriptions.
