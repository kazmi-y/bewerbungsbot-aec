# parser.py
# pdfplumber reads the embedded text layer of PDF (not OCR/computer vision)
# It is the best library for layout-heavy German CVs with two-column tables
# python-docx handles .docx files by iterating paragraph objects

import pdfplumber
from docx import Document

def extract_from_pdf(uploaded_file) -> str:
    """
    Takes a Streamlit UploadedFile object (PDF).
    Returns all text as a single string, pages joined by newline.
    Generator expression used for memory efficiency - one page at a time.
    """

    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join(
            page.extract_text() for page in pdf.pages
            if page.extract_text() is not None
        )

def extract_from_docx(uploaded_file) -> str:
    """
    Takes a Streamlit UploadedFile object (DOCX).
    Returns all paragraph text joined by newline.
    """
    doc = Document(uploaded_file)
    return "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
        if paragraph.text.strip() != ""
    )

def extract_document_text(uploaded_file) -> str:
    """
    Master function - detects file type automatically and routes to correct
    extractor.
    This is the only function app.py will ever call from this module.
    """
    filename = uploaded_file.name.lower().strip()

    if filename.endswith(".pdf"):
        return extract_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_from_docx(uploaded_file)
    else:
        raise ValueError(
            f"Nicht unterstütztes Dateiformat: {filename}."
            f"Nur PDF und DOCX erlaubt."
        )