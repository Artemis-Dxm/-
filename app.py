from flask import Flask, request, jsonify, send_from_directory
import io
import PyPDF2
from docx import Document
import httpx
import json
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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

async def call_glm(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers=headers,
            json=data
        )
        result = response.json()
        return result["choices"][0]["message"]["content"]

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "detail": "No file provided"}), 400
        
        file = request.files['file']
        content = file.read()
        text = parse_document(content, file.filename)
        return jsonify({"success": True, "content": text, "filename": file.filename}), 200
    except Exception as e:
        return jsonify({"success": False, "detail": str(e)}), 400

@app.route('/api/understand', methods=['POST'])
def understand():
    try:
        data = request.get_json()
        content = data.get('content', '')
        api_key = data.get('api_key', '')
        
        if not content or not api_key:
            return jsonify({"success": False, "detail": "Missing content or api_key"}), 400
        
        prompt = f"""你是一位专业的教学设计专家。请仔细阅读以下教学文档，理解其核心观点、教学理念和设计思路。

教学文档内容：
{content}

请提取并总结：
1. 文档的核心观点和主题
2. 教学方法或理念
3. 教学设计的主要特点
4. 关键概念和知识点

请用清晰的结构化方式呈现。"""
        
        import asyncio
        result = asyncio.run(call_glm(prompt, api_key))
        return jsonify({"success": True, "summary": result}), 200
    except Exception as e:
        return jsonify({"success": False, "detail": str(e)}), 500

@app.route('/api/review', methods=['POST'])
def review():
    try:
        data = request.get_json()
        content = data.get('content', '')
        teaching_summary = data.get('teaching_summary', '')
        api_key = data.get('api_key', '')
        score = data.get('score', 5)
        
        if not content or not teaching_summary or not api_key:
            return jsonify({"success": False, "detail": "Missing required fields"}), 400
        
        prompt = f"""你是一位专业的教学审核专家。你已经学习过以下教学文档的观点和理念：

【已学习的教学文档要点】
{teaching_summary}

现在请审核以下文档，运用你学到的知识进行评价：

【待审核文档】
{content}

【审核打分】
{score}/10分

请从以下角度进行审核：
1. 与已学习教学理念的一致性
2. 文档的优点和亮点
3. 存在的问题和改进建议
4. 具体可行的修改建议

请给出详细、建设性的反馈。"""
        
        import asyncio
        result = asyncio.run(call_glm(prompt, api_key))
        return jsonify({"success": True, "review": result}), 200
    except Exception as e:
        return jsonify({"success": False, "detail": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
