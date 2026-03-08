import httpx
import json
from typing import Optional, List, Dict

class AIService:
    def __init__(self, api_url: str = "https://open.bigmodel.cn/api/paas/v4"):
        self.api_url = api_url
    
    async def understand_teaching_doc(self, content: str, api_key: str) -> str:
        prompt = f"""你是一位专业的教学设计专家。请仔细阅读以下教学文档，理解其核心观点、教学理念和设计思路。

教学文档内容：
{content}

请提取并总结：
1. 文档的核心观点和主题
2. 教学方法或理念
3. 教学设计的主要特点
4. 关键概念和知识点

请用清晰的结构化方式呈现。"""
        
        return await self._call_glm(prompt, api_key)
    
    async def review_document(self, review_content: str, teaching_summary: str, api_key: str) -> str:
        prompt = f"""你是一位专业的教学审核专家。你已经学习过以下教学文档的观点和理念：

【已学习的教学文档要点】
{teaching_summary}

现在请审核以下文档，运用你学到的知识进行评价：

【待审核文档】
{review_content}

请从以下角度进行审核：
1. 与已学习教学理念的一致性
2. 文档的优点和亮点
3. 存在的问题和改进建议
4. 具体可行的修改建议

请给出详细、建设性的反馈。"""
        
        return await self._call_glm(prompt, api_key)
    
    async def _call_glm(self, prompt: str, api_key: str) -> str:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "glm-4",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=data
            )
            result = response.json()
            return result["choices"][0]["message"]["content"]
