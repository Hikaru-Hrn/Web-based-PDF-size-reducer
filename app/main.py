import os
import shutil
import uuid

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .utils import compress_pdf

app = FastAPI()

# Монтируем статику и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/compress")
async def handle_compression(request: Request, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": "Ошибка: Пожалуйста, выберите PDF файл.",
                "success": False,
            },
        )

    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"raw_{file_id}.pdf")
    output_path = os.path.join(UPLOAD_DIR, f"compressed_{file_id}.pdf")

    # Сохраняем загруженный файл
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Сжимаем
    success = compress_pdf(input_path, output_path)

    if success:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": f"Файл {file.filename} успешно сжат!",
                "success": True,
                "download_link": f"/download/{file_id}",
            },
        )
    else:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": "Произошла ошибка при обработке файла.",
                "success": False,
            },
        )


@app.get("/download/{file_id}")
async def download_file(file_id: str):
    path = os.path.join(UPLOAD_DIR, f"compressed_{file_id}.pdf")
    return FileResponse(path, filename="compressed_document.pdf")
