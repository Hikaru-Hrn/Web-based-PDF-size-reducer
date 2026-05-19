import os
import subprocess


def compress_pdf(input_path: str, output_path: str):
    """
    Использует Ghostscript для сжатия PDF.
    Настройка /screen дает максимальное сжатие (72 dpi).
    """
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/screen",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path,
    ]

    try:
        subprocess.run(gs_command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
