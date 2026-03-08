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

async def review_document(review_content, teaching_summary, api_key, score=5):
    prompt = f"""你是一位专业的教学审核专家。你已经学习过以下教学文档的观点和理念：

【已学习的教学文档要点】
{teaching_summary}

现在请审核以下文档，运用你学到的知识进行评价：

【待审核文档】
{review_content}

【审核打分】
{score}/10分

请从以下角度进行审核：
1. 与已学习教学理念的一致性
2. 文档的优点和亮点
3. 存在的问题和改进建议
4. 具体可行的修改建议

请给出详细、建设性的反馈。"""
    
    return await call_glm(prompt, api_key)

def main(request):
    if request.method == 'POST':
        try:
            data = request.get_json()
            content = data.get('content', '')
            teaching_summary = data.get('teaching_summary', '')
            api_key = data.get('api_key', '')
            score = data.get('score', 5)
            
            if not content or not teaching_summary or not api_key:
                return json.dumps({"success": False, "detail": "Missing required fields"}), 400
            
            import asyncio
            result = asyncio.run(review_document(content, teaching_summary, api_key, score))
            return json.dumps({"success": True, "review": result}), 200
        except Exception as e:
            return json.dumps({"success": False, "detail": str(e)}), 500
    
    return json.dumps({"message": "Use POST"}), 200
