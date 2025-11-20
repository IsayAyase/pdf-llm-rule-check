import pdfplumber
from fastapi import UploadFile
import io

async def extract_text_from_uploaded_pdf(file: UploadFile) -> str:
    """
    Extracts text from a PDF uploaded via FastAPI (UploadFile).
    Works only for text-based PDFs.
    """
    # Read bytes from the uploaded file
    pdf_bytes = await file.read()

    text = []

    # pdfplumber can open from a byte stream
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text.append(extracted)

    return "\n".join(text)
