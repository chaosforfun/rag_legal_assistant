from typing import List

import requests

from .config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL

class LLMClient:
    def __init__(self):
        if not DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY is not set")

    def generate(self, question: str, contexts: List[str]) -> str:
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
