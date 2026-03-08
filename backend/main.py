from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import base64

from parser import DocumentParser
from ai_service import AIService

app = FastAPI(title="文档审核助手")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_service = AIService()

class ReviewRequest(BaseModel):
    content: str
    teaching_summary: str
    api_key: str

class UnderstandRequest(BaseModel):
    content: str
    api_key: str

@app.get("/")
async def root():
    return {"message": "文档审核助手 API", "version": "1.0.0"}

@app.post("/api/understand")
async def understand_teaching_doc(request: UnderstandRequest):
    try:
        result = await ai_service.understand_teaching_doc(
            request.content, 
            request.api_key
        )
        return {"success": True, "summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/review")
async def review_document(request: ReviewRequest):
    try:
        result = await ai_service.review_document(
            request.content,
            request.teaching_summary,
            request.api_key
        )
        return {"success": True, "review": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = DocumentParser.parse(content, file.filename)
        return {"success": True, "content": text, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
