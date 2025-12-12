import io
from pypdf import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file provided as bytes.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
