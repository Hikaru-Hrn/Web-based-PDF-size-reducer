import os
from celery import Celery
# Импортируем нашу новую чистую бизнес-логику!
from pdf_core import compress_pdf

# 1. Инициализация Celery (возвращаем код, который был у тебя раньше)
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',  # Убедись, что тут имя сервиса из docker-compose, а не 127.0.0.1
    backend='redis://redis:6379/0'
)


# 2. Сама задача
@celery_app.task(bind=True, name="app.worker.compression_task")
def compression_task(self, input_path, output_path, quality):
    try:
        # Вся "грязная" работа скрыта в нашем независимом пакете core
        result_path = compress_pdf(input_path, output_path, quality)
        return {"status": "completed", "output": result_path}

    except CorePDFError as e:
        # Перехватываем ошибки именно нашей бизнес-логики (например, не тот формат)
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise e

    except Exception as e:
        # Ловим непредвиденные системные сбои
        self.update_state(state="FAILURE", meta={"error": f"Внутренняя ошибка: {str(e)}"})
        raise e