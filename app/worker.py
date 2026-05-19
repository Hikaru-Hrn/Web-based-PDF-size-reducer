import os
import subprocess

from celery import Celery

celery_app = Celery(
    "tasks", broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0"
)


@celery_app.task(bind=True)
def compression_task(self, input_path, output_path, quality):
    quality_map = {"low": "/screen", "medium": "/ebook", "high": "/printer"}
    gs_settings = quality_map.get(quality, "/screen")

    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={gs_settings}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path,
    ]

    try:
        subprocess.run(cmd, check=True)
        return {"status": "completed", "output": output_path}
    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise e
