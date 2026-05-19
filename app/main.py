import os
import uuid

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .worker import celery_app, compression_task

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/compress")
async def start_compression(file: UploadFile = File(...), quality: str = Form("low")):
    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"in_{file_id}.pdf")
    output_path = os.path.join(UPLOAD_DIR, f"out_{file_id}.pdf")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Отправляем задачу в очередь
    task = compression_task.delay(input_path, output_path, quality)
    return JSONResponse({"task_id": task.id})


@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return {"status": "SUCCESS", "download_url": f"/download/{task_id}"}
    elif task.state == "FAILURE":
        return {"status": "FAILURE", "error": str(task.info)}
    return {"status": task.state}


@app.get("/download/{task_id}")
async def download(task_id: str):
    task = celery_app.AsyncResult(task_id)
    path = task.result.get("output")
    return FileResponse(path, filename="compressed.pdf")
