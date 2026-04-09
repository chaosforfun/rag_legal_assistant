import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def validate_config():
    """
    验证必要的配置项是否存在
    返回验证结果和错误信息列表
    """
    from rag_assistant.config import DATABASE_URL, DEEPSEEK_API_KEY

    errors = []

    # 检查数据库配置
    if not DATABASE_URL:
        errors.append("DATABASE_URL 未设置，请检查环境变量或 .env 文件")

    # 检查 DeepSeek API 密钥
    if not DEEPSEEK_API_KEY:
        errors.append("DEEPSEEK_API_KEY 未设置，请检查环境变量或 .env 文件")
        logger.warning("DEEPSEEK_API_KEY 未设置，LLM 功能将不可用")

    return len(errors) == 0, errors


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    在应用启动和关闭时执行必要的操作
    """
    # 启动时验证配置
    logger.info("正在启动 RAG Assistant 服务...")
    is_valid, errors = validate_config()

    if not is_valid:
        for error in errors:
            logger.error(f"配置错误: {error}")
        # 记录错误但不阻止启动，因为某些功能可能仍然可用
        logger.warning("检测到配置问题，部分功能可能不可用")
    else:
        logger.info("配置验证通过")

    yield

    # 关闭时的清理操作
    logger.info("正在关闭 RAG Assistant 服务...")


def get_uvicorn_config():
    """
    从环境变量或配置文件获取 uvicorn 运行配置
    """
    import os

    from rag_assistant.config import BASE_DIR

    # 从环境变量读取配置，提供合理的默认值
    host = os.getenv("UVICORN_HOST", "0.0.0.0")
    port = int(os.getenv("UVICORN_PORT", "8000"))
    reload = os.getenv("UVICORN_RELOAD", "true").lower() == "true"
    log_level = os.getenv("UVICORN_LOG_LEVEL", "info")

    # 开发环境下启用 reload，生产环境建议关闭
    reload_dirs = [str(BASE_DIR / "rag_assistant")] if reload else None

    return {
        "host": host,
        "port": port,
        "reload": reload,
        "log_level": log_level,
        "reload_dirs": reload_dirs
    }


def main():
    """
    主入口函数，负责启动 uvicorn 服务器
    包含异常处理以确保优雅的错误报告
    """
    try:
        # 获取配置
        config = get_uvicorn_config()

        logger.info(f"启动服务器 - 主机: {config['host']}, 端口: {config['port']}, 热重载: {config['reload']}")

        # 启动 uvicorn 服务器
        uvicorn.run(
            "rag_assistant.api:app",
            host=config["host"],
            port=config["port"],
            reload=config["reload"],
            log_level=config["log_level"],
            reload_dirs=config["reload_dirs"]
        )
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭服务器...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
