import io
import PyPDF2
from docx import Document
from typing import Optional

class DocumentParser:
    @staticmethod
    def parse(file_content: bytes, filename: str) -> str:
        ext = filename.lower().split('.')[-1]
        
        if ext == 'pdf':
            return DocumentParser._parse_pdf(file_content)
        elif ext in ['docx', 'doc']:
            return DocumentParser._parse_docx(file_content)
        elif ext in ['txt', 'md']:
            return file_content.decode('utf-8', errors='ignore')
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
    
    @staticmethod
    def _parse_pdf(content: bytes) -> str:
        pdf_file = io.BytesIO(content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    @staticmethod
    def _parse_docx(content: bytes) -> str:
        doc_file = io.BytesIO(content)
        doc = Document(doc_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
