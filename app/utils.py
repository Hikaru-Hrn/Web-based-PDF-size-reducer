import os
import subprocess


def compress_pdf(input_path: str, output_path: str, quality: str = "screen"):
    # Качество: screen (72dpi), ebook (150dpi), printer (300dpi)
    quality_map = {"low": "/screen", "medium": "/ebook", "high": "/printer"}
    gs_settings = quality_map.get(quality, "/screen")

    gs_command = [
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

    try:
        subprocess.run(gs_command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
