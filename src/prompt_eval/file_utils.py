"""Utility functions for extracting content from various file formats.

INTERNAL MODULE: Used for extracting file content for prompt caching.
"""

from pathlib import Path
from pypdf import PdfReader


def extract_file_content(file_path: str | Path) -> str:
    """
    Extract text content from a file.
    Supports multiple formats: .pdf, .md, .txt, and other text files.

    Args:
        file_path: Path to the file

    Returns:
        Extracted text content as a single string

    Raises:
        FileNotFoundError: If the file doesn't exist
        Exception: If content extraction fails
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine file type by extension
    suffix = file_path.suffix.lower()

    try:
        if suffix == ".pdf":
            return _extract_pdf(file_path)
        else:
            # For all other files (.md, .txt, etc.), read as text
            return _extract_text(file_path)
    except Exception as e:
        raise Exception(f"Failed to extract content from {file_path}: {e}")


def _extract_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_path)
    text_parts = []

    for page_num, page in enumerate(reader.pages, 1):
        page_text = page.extract_text()
        if page_text.strip():
            text_parts.append(page_text)

    return "\n\n".join(text_parts)


def _extract_text(file_path: Path) -> str:
    """Extract text from a plain text file (markdown, txt, etc.)."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
