import os
from celery import Celery
from pdf_core import compress_pdf

celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)


@celery_app.task(bind=True, name="app.worker.compression_task")
def compression_task(self, input_path, output_path, quality):
    try:
        result_path = compress_pdf(input_path, output_path, quality)
        return {"status": "completed", "output": result_path}

    except CorePDFError as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise e

    except Exception as e:
        # Ловим непредвиденные системные сбои
        self.update_state(state="FAILURE", meta={"error": f"Внутренняя ошибка: {str(e)}"})
        raise e