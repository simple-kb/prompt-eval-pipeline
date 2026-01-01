"""Utility functions for extracting text from PDF files.

INTERNAL MODULE: Used for extracting PDF content for prompt caching.
"""

from pathlib import Path
from pypdf import PdfReader


def extract_pdf_text(pdf_path: str | Path) -> str:
    """
    Extract all text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text content as a single string

    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        Exception: If PDF extraction fails
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        reader = PdfReader(pdf_path)
        text_parts = []

        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            if page_text.strip():
                text_parts.append(page_text)

        return "\n\n".join(text_parts)

    except Exception as e:
        raise Exception(f"Failed to extract text from PDF {pdf_path}: {e}")
