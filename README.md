# GridWatch

A simple CRUD API to model power grid components and IoT devices measuring
power consumption.

## Overview

### Description

The application was written as the solution to a programming challenge. The
original formulation of the challenge can be found in [REQUIREMENTS.md](/REQUIREMENTS.md).

A documentation of the development process and the decisions made in
the process can be found in [DEVLOG.md](/DEVLOG.md).

Tech Stack: FastAPI, SQLAlchemy, PostgreSQL, Docker.

### Installation

1. Install cargo (for uv):
[https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)

1. Install uv:
[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

1. Clone the repository:

  ```bash
  git clone https://github.com/alvarotroya/gridwatch
  ```

1. Navigate to the project directory:

  ```bash
  cd gridwatch
  ```

1. Set up dev environment:

  ```bash
  uv python install 3.12
  uv venv
  source .venv/bin/activate
  ```

1. Install pre-commit hooks:

  ```bash
  pre-commit install --hook-type pre-commit --hook-type pre-push
  ```

1. Set up database credentials

  ```bash
  cp .env-example .env
  ```

1. Start the database

  ```bash
  docker-compose up -d
  ```

1. Start the server

  ```bash
  fastapi dev gridwatch/main.py
  ```

1. Visit the OpenAPI documentation at [localhost:8000/docs](localhost:8000/docs).

## Future development

- [ ] Profile the endpoints using [yappi](https://github.com/sumerc/yappi).
- [ ] Load test the `POST` measurements endpoints to using [Locust](https://locust.io/).
- [ ] Use [Celery](https://github.com/celery/celery) and RabbitMQ/Redis to
process measurements asynchronously via a queue.
- [ ] Measure latency:
  - From the moment the measurement is made
  - To the moment the measurement is sent and placed into the queue.
  - To the moment the measurement is picked up from the queue.
  - To the moment the measurement persisted on the DB.

- Questions to answer:
  - How well can a single server instance handle the load?
  - How well can a single server running the application in multiple threads
  handle the load?
  - How well can multiple servers (2,3,4,...) running behind a load balancer
  handle the load? Does the database become the bottleneck?
  - How well can a single server and the same setup handle the load when
  queueing measurements for writes instead of persisiting them directly?
  - How does latency change between both setups?
