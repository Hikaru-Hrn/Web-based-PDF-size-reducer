# Web-based PDF Size Reducer
**English version** | [Русская версия](README.md)

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Celery](https://img.shields.io/badge/Celery-Message_Broker-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

An asynchronous microservice for compressing PDF documents. The project is designed with the separation of concerns principle in mind: the business logic is completely isolated from the web infrastructure.

## Project Architecture

The project is divided into several key layers:

1. **`packages/core/` (Core)** — An independent Python package (`pdf_core`). Contains validation logic and Ghostscript interaction. It is completely decoupled from web frameworks and message queues.
2. **FastAPI (`app/main.py`)** — API Gateway. Responsible solely for handling HTTP file uploads and request routing.
3. **Celery Worker (`app/worker.py`)** — Background task executor. Fetches tasks from the queue and utilizes the `pdf_core` package for heavy computations without blocking the main web server.
4. **Redis** — Message broker for communication between FastAPI and Celery.

## Getting Started (Docker)

The project is fully containerized and can be launched with a single command. Container communication is configured via an internal Docker bridge network to ensure 100% cross-platform compatibility.

**Prerequisites:**
- Docker and Docker Compose
- `make` utility

**Unified Command Interface (Makefile):**
```text
  make setup      - Install local development dependencies
  make test       - Run unit and integration tests
  make run        - Start the project in Docker (API, Celery, Redis)
  make run-build  - Rebuild containers and start the project
  make down       - Stop and remove Docker containers
  make clean      - Remove Python caches and temporary files