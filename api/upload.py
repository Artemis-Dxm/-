import io
import PyPDF2
from docx import Document
import json

def parse_document(file_content, filename):
    ext = filename.lower().split('.')[-1]
    
    if ext == 'pdf':
        pdf_file = io.BytesIO(file_content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif ext in ['docx', 'doc']:
        doc_file = io.BytesIO(file_content)
        doc = Document(doc_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    elif ext in ['txt', 'md']:
        return file_content.decode('utf-8', errors='ignore')
    else:
        raise ValueError(f"不支持的文件格式: {ext}")

def main(request):
    if request.method == 'POST':
        try:
            file = request.files.get('file')
            if not file:
                return json.dumps({"success": False, "detail": "No file provided"}), 400
            
            content = file.read()
            text = parse_document(content, file.filename)
            return json.dumps({"success": True, "content": text, "filename": file.filename}), 200
        except Exception as e:
            return json.dumps({"success": False, "detail": str(e)}), 400
    
    return json.dumps({"message": "Use POST to upload"}), 200
