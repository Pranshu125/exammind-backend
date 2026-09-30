import re
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file using pypdf (pure Python, no C++ compilers needed).
    """
    try:
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                # Clean up excessive newlines and whitespace
                text = re.sub(r'\s+', ' ', text).strip()
                full_text += text + "\n"
        return full_text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")
