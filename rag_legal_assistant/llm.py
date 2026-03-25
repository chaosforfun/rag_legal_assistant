from typing import List

import requests

from .config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL

class LLMClient:
    def __init__(self):
        self.mock_mode = not DEEPSEEK_API_KEY
        if self.mock_mode:
            print("Warning: DEEPSEEK_API_KEY is not set, running in mock mode")

    def generate(self, question: str, contexts: List[str]) -> str:
        if self.mock_mode:
            if not contexts:
                return "系统提示：DEEPSEEK_API_KEY 未配置。请在 .env 文件中设置您的 DeepSeek API 密钥后再使用问答功能。\n\n同时，数据库中暂无法规数据，请先运行 python scripts/ingest_data.py 导入数据。"
            context_text = "\n".join([f"[{idx}] {ctx[:200]}..." for idx, ctx in enumerate(contexts, 1)])
            return f"[模拟模式] 请设置 DEEPSEEK_API_KEY 环境变量以启用真实回答。\n\n问题: {question}\n\n找到的参考资料:\n{context_text}\n\n提示: 请设置 DEEPSEEK_API_KEY 环境变量后重启服务。"

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
