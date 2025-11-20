from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from lib.pdf_to_text import extract_text_from_uploaded_pdf
from services.llm import check_rules_with_gemini

router = APIRouter(
    prefix="/check",
    )

@router.post("/pdf")
async def upload_pdf_and_text(
    file: UploadFile = File(...),
    rules: str = Form(...)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    if not rules:
        raise HTTPException(status_code=400, detail="Rules must not be empty")
    
    rules = [text.strip() for text in rules.split(",")]

    documents_text = await extract_text_from_uploaded_pdf(file)
    result = check_rules_with_gemini(rules, documents_text)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "rules": rules,
        "result": result
    }
