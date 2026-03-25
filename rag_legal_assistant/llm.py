from typing import List

import requests

from .config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL


class LLMClient:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_base = DEEPSEEK_API_BASE
        self.model = DEEPSEEK_MODEL

    def generate(self, question: str, contexts: List[str]) -> str:
        if not self.api_key:
            return "系统提示：DEEPSEEK_API_KEY 未配置。请在 .env 文件中设置您的 DeepSeek API 密钥后再使用问答功能。"

        try:
            prompt = f"问题: {question}\n\n参考资料:\n"
            for idx, ctx in enumerate(contexts, 1):
                prompt += f"[{idx}] {ctx[:500]}\n"
            prompt += "\n请基于参考资料生成中文回答，并在句末标注引用编号。"

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "你是法律法规助手，只能基于给定参考资料回答"},
                    {"role": "user", "content": prompt},
                ],
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            resp = requests.post(f"{self.api_base}/v1/chat/completions", json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"API请求失败: {str(e)}"
        except Exception as e:
            return f"生成回答时出错: {str(e)}"
