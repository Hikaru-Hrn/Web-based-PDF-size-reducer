# Web-based PDF size Reducer
[English version](README.en.md) | **Русская версия**

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Celery](https://img.shields.io/badge/Celery-Message_Broker-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

Асинхронный микросервис для сжатия PDF-документов. Проект разделен на независимое ядро обработки (Python-пакет) и инфраструктурный слой (FastAPI + Celery + Redis).

## Архитектура проекта

Проект спроектирован с учетом принципов чистой архитектуры и разделения ответственности:

1. **`packages/core/pdf_core`** — Независимое ядро (Domain Logic). Обертка над Ghostscript. Не имеет привязки к веб-фреймворкам, полностью покрыта unit-тестами.
2. **`app/main.py`** — API-шлюз на FastAPI. Отвечает только за прием файлов и маршрутизацию запросов.
3. **`app/worker.py`** — Фоновый воркер Celery. Выполняет тяжелую задачу сжатия, используя пакет `pdf_core`, не блокируя основной веб-сервер.
4. **Redis** — Брокер сообщений для связи FastAPI и Celery.

## Запуск проекта (Docker)

Проект полностью контейнеризирован и запускается одной командой. Взаимодействие контейнеров настроено через внутреннюю сеть Docker (bridge network) для 100% кроссплатформенности.

**Требования:**
- Docker и Docker Compose
- Утилита `make`

**Единая поверхность команд (Makefile):**
```text
  make setup      - Установить локальные зависимости
  make test       - Запустить unit и интеграционные тесты
  make run        - Запустить весь проект в Docker (API, Celery, Redis)
  make run-build  - Пересобрать контейнеры и запустить проект
  make down       - Остановить и удалить контейнеры
  make clean      - Очистить кэши Python