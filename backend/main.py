from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="Code PDF Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.services.detector import LanguageDetector
from backend.services.pdf_maker import PdfGenerator
from backend.services.ai_service import AIService
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import Response

class CodeItem(BaseModel):
    filename: str
    code: str
    language: Optional[str] = None
    description: Optional[str] = None

class DetectRequest(BaseModel):
    code: str

class GeneratePdfRequest(BaseModel):
    items: List[CodeItem]
    title: Optional[str] = "Code Documentation"

@app.post("/api/detect-language")
def detect_language(request: DetectRequest):
    lang = LanguageDetector.detect_language(request.code)
    return {"language": lang}

@app.post("/api/ai-describe")
def ai_describe(request: DetectRequest):
    desc = AIService.generate_description(request.code)
    return {"description": desc}

@app.post("/api/generate-pdf")
def generate_pdf(request: GeneratePdfRequest):
    # Ensure languages are detected if missing
    items_data = []
    for item in request.items:
        lang = item.language
        if not lang or lang == "Auto":
            lang = LanguageDetector.detect_language(item.code)
        
        items_data.append({
            "filename": item.filename,
            "code": item.code,
            "language": lang,
            "description": item.description
        })

    pdf_generator = PdfGenerator()
    pdf_bytes = pdf_generator.generate_pdf(items_data, title=request.title)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=code_document.pdf"}
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
