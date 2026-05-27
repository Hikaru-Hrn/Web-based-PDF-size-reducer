import os
from .exceptions import InvalidPDFError


def validate_pdf(file_path: str) -> None:
    """
    Проверяет существование файла и его базовую валидность.
    """
    if not os.path.exists(file_path):
        raise InvalidPDFError(f"Файл не найден: {file_path}")

    if not os.path.isfile(file_path):
        raise InvalidPDFError(f"Указанный путь не является файлом: {file_path}")

    if not file_path.lower().endswith('.pdf'):
        raise InvalidPDFError("Файл должен иметь расширение .pdf")

    if os.path.getsize(file_path) == 0:
        raise InvalidPDFError("Файл пуст (размер 0 байт)")