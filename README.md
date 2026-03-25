# 法规知识 RAG 助手

## 项目简介

- 目标：为法律/合规人员提供快速法规检索与问答
- 架构：FastAPI 服务 + 向量数据库（PostgreSQL + pgvector/FAISS）+ Vue 前端 + DeepSeek 大模型
- 流程：
  1. 数据导入：解析法规文本，生成向量并存入数据库
  2. 检索：根据用户问题向量化检索相似条文
  3. 生成：将检索到的条文交给 DeepSeek 模型生成回答

## 目录结构

```
rag_legal_assistant/
├── README.md
├── requirements.txt
├── data/
│   └── legal/
├── artifacts/
├── rag_legal_assistant/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── data_loader.py
│   ├── embedding.py
│   ├── llm.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── vector_store.py
│   └── main.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.js
│       └── App.vue
└── scripts/
    ├── ingest_data.py
    └── run_server.sh
```

## 使用说明

1. 准备法律法规文本到 `data/legal` 目录
2. `python scripts/ingest_data.py` 向数据库写入向量
3. `uvicorn rag_legal_assistant.api:app --reload`
4. 前端目录执行 `npm install && npm run dev`

## 环境变量

- `DATABASE_URL`: PostgreSQL 连接（包含 pgvector 支持）
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `DEEPSEEK_API_BASE`: DeepSeek API 基础地址（默认 https://api.deepseek.com）
- `DEEPSEEK_MODEL`: 指定模型（默认 deepseek-chat）
- `LEGAL_DATA_DIR`: 自定义法规数据目录
- `EMBED_MODEL_NAME`: SentenceTransformer 模型名
- `VECTOR_DIM`: 向量维度（需与模型匹配）
