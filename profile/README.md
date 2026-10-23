# Kionga

**Machine learning, data and AI agents on infrastructure you control.**

Kionga is an open-source, self-hosted platform that gives your team one place to
build, train, serve and observe models and AI agents, behind a single console and
API, running in your own environment.

## What Kionga does

- **Workspaces.** Personal JupyterLab and browser IDE workspaces with Git, project
  templates and resource limits set by your administrators.
- **Pipelines.** Define container pipelines once and run them with parameters,
  schedules, retries, timeouts, resource limits and a live run view.
- **Models and serving.** Track experiments, register models, promote them through
  quality gates and serve them with canary releases and rollback.
- **Features.** Online and offline features with a Feast-compatible API, or connect
  the feature store you already run.
- **AI agents.** Deploy agents with persistent sessions, tools, tracing and token
  cost accounting, built with LangGraph or your own framework.
- **Real-time processing.** Stream events through Kafka to online features and live
  models or agents.

**Secure by default:** single sign-on, role and policy based access, deny-by-default
quotas and an immutable audit trail. **Your infrastructure:** a laptop, a single
server or managed Kubernetes on AWS, Google Cloud or Azure. **Open standards:**
MLflow, Prefect, Kafka, PostgreSQL, S3-compatible storage and an OpenAI-compatible
LLM gateway.

## Get started

- [Documentation](https://kiongahq.github.io/docs/)
- [Install Kionga](https://kiongahq.github.io/docs/getting-started/installation/)
- [Engineering handbook](https://kiongahq.github.io/docs/engineering/), for people
  who change Kionga's code

## Repositories

| Repository | What it is |
| --- | --- |
| [platform](https://github.com/kiongahq/platform) | Control plane: gateway API, web console, operator and supporting services |
| [deploy](https://github.com/kiongahq/deploy) | Run Kionga with Docker Compose, on a single server or on Kubernetes |
| [sdk-python](https://github.com/kiongahq/sdk-python) | Python SDK for notebooks, scripts and agents |
| [agent-runtime](https://github.com/kiongahq/agent-runtime) | Agent serving, feature materialization and real-time processing |
| [pipeline-runner](https://github.com/kiongahq/pipeline-runner) | Runs pipelines as containers through Prefect |
| [serving](https://github.com/kiongahq/serving) | Model serving manager |
| [trace-proxy](https://github.com/kiongahq/trace-proxy) | LLM egress proxy with tracing |
| [workspace](https://github.com/kiongahq/workspace) | Jupyter workbench, browser IDE and project CLI |
| [contracts](https://github.com/kiongahq/contracts) | Versioned schemas shared by the components |
| [docs](https://github.com/kiongahq/docs) | Product documentation and engineering handbook |

Kionga is licensed under the [MIT License](https://github.com/kiongahq/.github/blob/main/LICENCE).
