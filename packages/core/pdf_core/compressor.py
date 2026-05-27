import subprocess
from .exceptions import PDFCompressionError
from .validator import validate_pdf


def compress_pdf(input_path: str, output_path: str, quality: str = "medium") -> str:
    """
    Сжимает PDF файл.

    Args:
        input_path: Путь к исходному PDF файлу.
        output_path: Путь для сохранения сжатого файла.
        quality: Степень сжатия ('low', 'medium', 'high').

    Returns:
        str: Путь к итоговому (сжатому) файлу.

    Raises:
        InvalidPDFError: Если исходный файл не прошел валидацию.
        PDFCompressionError: При ошибке выполнения Ghostscript.
    """
    # 1. Валидируем входные данные
    validate_pdf(input_path)

    # 2. Настраиваем параметры
    quality_map = {
        "low": "/screen",  # Максимальное сжатие, 72 dpi
        "medium": "/ebook",  # Баланс, 150 dpi
        "high": "/printer"  # Минимальное сжатие, 300 dpi
    }
    gs_settings = quality_map.get(quality, "/ebook")

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

    # 3. Выполняем сжатие с перехватом системных ошибок
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
    except subprocess.CalledProcessError as e:
        # Прячем системную ошибку subprocess и отдаем понятную доменную
        error_msg = e.stderr.decode('utf-8', errors='ignore') or str(e)
        raise PDFCompressionError(f"Сбой Ghostscript: {error_msg}")