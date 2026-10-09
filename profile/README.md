# Kionga

MIT-licensed, self-hosted platform for building, deploying and operating ML models and AI agents:
projects and Jupyter/IDE workspaces, versioned pipeline DAGs with schedules, model
registry and serving, agents with memory, tools and tracing, feature stores, logs and
fine-grained access policies, in one console.

**Start here:** [Documentation](https://kiongahq.github.io/docs/) ·
[Run it locally](https://github.com/kiongahq/deploy#run-it-locally)

## How the pieces connect

| Repository | Role |
| --- | --- |
| [platform](https://github.com/kiongahq/platform) | Control plane: gateway API and console, auth and IAM, store, scheduler, pipeline execution, logs, operator |
| [contracts](https://github.com/kiongahq/contracts) | Versioned schemas the components agree on |
| [sdk-python](https://github.com/kiongahq/sdk-python) | Python SDK for notebooks, scripts and agents |
| [agent-runtime](https://github.com/kiongahq/agent-runtime) | Serves agents; feature materializer; realtime processor |
| [pipeline-runner](https://github.com/kiongahq/pipeline-runner) | Executes pipeline DAGs as containers |
| [serving](https://github.com/kiongahq/serving) | Model serving manager |
| [trace-proxy](https://github.com/kiongahq/trace-proxy) | OpenAI-compatible LLM egress with tracing |
| [workspace](https://github.com/kiongahq/workspace) | Jupyter workbench, browser IDE, workspace CLI |
| [deploy](https://github.com/kiongahq/deploy) | Runs it all: Compose, single VM, Helm, kind |
| [docs](https://github.com/kiongahq/docs) | The documentation site |

Components share code only through [contracts](https://github.com/kiongahq/contracts)
and released packages, talk to each other over the platform's HTTP API, and ship as
images under `ghcr.io/kiongahq`. [deploy](https://github.com/kiongahq/deploy) builds
them from sibling checkouts for development and pins released digests for
production. Details: [Repositories](https://kiongahq.github.io/docs/overview/repositories/).
