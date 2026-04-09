#!/bin/bash
uvicorn rag_assistant.api:app --host 0.0.0.0 --port 8000
