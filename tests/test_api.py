from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Импортируем ваше FastAPI приложение
from app.main import app

client = TestClient(app)


@patch("app.main.compression_task.delay")
def test_upload_valid_pdf(mock_delay):
    """
    Проверка успешной загрузки PDF файла через API.
    """
    # 1. Настраиваем заглушку Celery: пусть она вернет фейковый ID задачи
    mock_task_result = MagicMock()
    mock_task_result.id = "test-task-12345"
    mock_delay.return_value = mock_task_result

    # 2. Создаем фейковый PDF-файл в памяти (не создавая его на диске)
    # Формат: ("имя_файла", b"содержимое_в_байтах", "MIME-тип")
    test_file = ("document.pdf", b"%PDF-1.4 test content", "application/pdf")

    # 3. Делаем POST-запрос к приложению
    # Примечание: если ваш эндпоинт загрузки называется по-другому (например, /upload),
    # измените "/" на "/upload".
    response = client.post(
        "/",
        files={"file": test_file},
        data={"quality": "medium"}  # Передаем параметр качества, если он у вас есть
    )

    # 4. Проверяем результат
    # Обычно при успешной загрузке FastAPI возвращает 200 OK
    assert response.status_code == 200

    # Проверяем, что в ответе есть наш фейковый ID задачи (или просто сам факт ответа)
    json_response = response.json()
    assert "task_id" in json_response
    assert json_response["task_id"] == "test-task-12345"

    # Проверяем, что FastAPI действительно вызвал Celery
    mock_delay.assert_called_once()


def test_upload_no_file():
    """
    Проверка поведения API при отсутствии файла в запросе.
    """
    # Делаем запрос без параметра files
    response = client.post("/", data={"quality": "low"})

    # FastAPI должен автоматически вернуть ошибку валидации 422 Unprocessable Entity
    assert response.status_code == 422