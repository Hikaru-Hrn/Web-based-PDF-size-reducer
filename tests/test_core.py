import pytest
import os
from unittest.mock import patch
from pdf_core.compressor import compress_pdf
from pdf_core.exceptions import InvalidPDFError, PDFCompressionError
from pdf_core.validator import validate_pdf


# --- Тесты для валидатора (validator.py) ---

# Файл не существует
def test_validate_pdf_not_found():
    with pytest.raises(InvalidPDFError, match="Файл не найден"):
        validate_pdf("fake_path/doc.pdf")


# неправильное расширение
def test_validate_pdf_wrong_extension(tmp_path):
    # tmp_path - встроенная фикстура pytest для создания временных файлов
    temp_file = tmp_path / "document.txt"
    temp_file.write_text("какой-то текст")

    with pytest.raises(InvalidPDFError, match="Файл должен иметь расширение .pdf"):
        validate_pdf(str(temp_file))

# файл пуст
def test_validate_pdf_empty_file(tmp_path):
    temp_file = tmp_path / "empty.pdf"
    temp_file.write_text("")  # Создаем пустой файл

    with pytest.raises(InvalidPDFError, match="Файл пуст"):
        validate_pdf(str(temp_file))


# --- Тесты для компрессора (compressor.py) ---

# Успешное сжатие
@patch("pdf_core.compressor.subprocess.run")
def test_compress_pdf_success(mock_subprocess, tmp_path):
    # тестовые данные
    input_file = tmp_path / "input.pdf"
    input_file.write_text("%PDF-1.4 test content")  # Имитируем непустой PDF
    output_file = tmp_path / "output.pdf"

    result = compress_pdf(str(input_file), str(output_file), "low")

    assert result == str(output_file)
    # Проверяем, что subprocess.run был вызван (то есть команда Ghostscript "отправлена")
    mock_subprocess.assert_called_once()

# Gs упал с системной ошибкой
@patch("pdf_core.compressor.subprocess.run")
def test_compress_pdf_ghostscript_error(mock_subprocess, tmp_path):
    import subprocess

    input_file = tmp_path / "input.pdf"
    input_file.write_text("%PDF-1.4 test content")
    output_file = tmp_path / "output.pdf"

    # имитация сбоя системы
    mock_subprocess.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd="gs",
        stderr=b"Some fatal Ghostscript error"
    )

    with pytest.raises(PDFCompressionError, match="Сбой Ghostscript"):
        compress_pdf(str(input_file), str(output_file), "medium")