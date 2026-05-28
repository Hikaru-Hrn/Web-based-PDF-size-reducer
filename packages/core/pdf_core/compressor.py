import subprocess
from .exceptions import PDFCompressionError
from .validator import validate_pdf


def compress_pdf(input_path: str, output_path: str, quality: str = "medium") -> str:
    """
        Сжимает PDF-файл с использованием Ghostscript.

        Эта функция является независимым ядром и может использоваться
        вне веб-интерфейса. Уровень сжатия влияет на итоговое DPI документа.

        Args:
            input_path (str): Абсолютный или относительный путь к исходному PDF.
            output_path (str): Путь, куда будет сохранен сжатый файл.
            quality (str): Уровень качества. Варианты: 'low' (72 dpi), 'medium' (150 dpi), 'high' (300 dpi).

        Returns:
            str: Путь к итоговому (сжатому) файлу.

        Raises:
            InvalidPDFError: Если исходный файл не существует или не является PDF.
            PDFCompressionError: Если процесс Ghostscript завершился с системной ошибкой.
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