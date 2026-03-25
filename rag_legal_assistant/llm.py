from typing import List

import requests

from .config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL

class LLMClient:
    def __init__(self):
        self.has_api_key = DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "your-api-key-here"

    def generate(self, question: str, contexts: List[str]) -> str:
        # 如果没有配置 API key，返回模拟回答（用于测试）
        if not self.has_api_key:
            return self._generate_mock_response(question, contexts)

        prompt = f"问题: {question}\n\n参考资料:\n"
        for idx, ctx in enumerate(contexts, 1):
            prompt += f"[{idx}] {ctx[:500]}\n"
        prompt += "\n请基于参考资料生成中文回答，并在句末标注引用编号。"

        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": "你是法律法规助手，只能基于给定参考资料回答"},
                {"role": "user", "content": prompt},
            ],
        }
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }
        resp = requests.post(f"{DEEPSEEK_API_BASE}/v1/chat/completions", json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def _generate_mock_response(self, question: str, contexts: List[str]) -> str:
        """生成模拟回答（用于测试）"""
        if not contexts:
            return "【演示模式】未找到相关法规资料，请先导入数据。"

        response = f"【演示模式 - 未配置 DeepSeek API】\n\n"
        response += f"根据您的问题「{question}」，找到以下相关法规：\n\n"

        for idx, ctx in enumerate(contexts, 1):
            response += f"[{idx}] {ctx[:300]}...\n\n"

        response += "提示：如需获取 AI 生成的专业回答，请在 .env 文件中配置有效的 DEEPSEEK_API_KEY。"
        return response
