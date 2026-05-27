from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)


# Проверка успешной загрузки PDF через API
@patch("app.main.compression_task.delay")
def test_upload_valid_pdf(mock_delay):
    # Заглушка Celery (вернет фейковый ID задачи)
    mock_task_result = MagicMock()
    mock_task_result.id = "test-task-12345"
    mock_delay.return_value = mock_task_result

    # фейковый PDF-файл в памяти
    test_file = ("document.pdf", b"%PDF-1.4 test content", "application/pdf")

    # POST-запрос к приложению
    response = client.post(
        "/compress",
        files={"file": test_file},
        data={"quality": "medium"}  # Передаем параметр качества, если он у вас есть
    )

    # Проверяем результат
    assert response.status_code == 200

    # Проверяем, что в ответе есть наш фейковый ID задачи (или просто сам факт ответа)
    json_response = response.json()
    assert "task_id" in json_response
    assert json_response["task_id"] == "test-task-12345"

    # Проверяем, что FastAPI действительно вызвал Celery
    mock_delay.assert_called_once()

# Проверка поведения API при отсутствии файла в запросе.
def test_upload_no_file():
    response = client.post("/compress", data={"quality": "low"})

    assert response.status_code == 422