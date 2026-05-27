class CorePDFError(Exception):
    """Базовый класс исключений для пакета pdf_core."""
    pass

class InvalidPDFError(CorePDFError):
    """Вызывается, если файл не найден или не является валидным PDF."""
    pass

class PDFCompressionError(CorePDFError):
    """Вызывается, если Ghostscript завершился с ошибкой."""
    pass