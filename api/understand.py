import json
import httpx

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

async def understand_teaching_doc(content, api_key):
    prompt = f"""你是一位专业的教学设计专家。请仔细阅读以下教学文档，理解其核心观点、教学理念和设计思路。

教学文档内容：
{content}

请提取并总结：
1. 文档的核心观点和主题
2. 教学方法或理念
3. 教学设计的主要特点
4. 关键概念和知识点

请用清晰的结构化方式呈现。"""
    
    return await call_glm(prompt, api_key)

def main(request):
    if request.method == 'POST':
        try:
            data = request.get_json()
            content = data.get('content', '')
            api_key = data.get('api_key', '')
            
            if not content or not api_key:
                return json.dumps({"success": False, "detail": "Missing content or api_key"}), 400
            
            import asyncio
            result = asyncio.run(understand_teaching_doc(content, api_key))
            return json.dumps({"success": True, "summary": result}), 200
        except Exception as e:
            return json.dumps({"success": False, "detail": str(e)}), 500
    
    return json.dumps({"message": "Use POST"}), 200
