"""
配置文件 - AI模型选择
"""
import os

# AI模型选择: "gemini" 或 "deepseek"
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")

# Gemini 配置
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-1.5-pro"

# DeepSeek 配置 (国内访问更稳定)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 请求超时设置（秒）
API_TIMEOUT = 30

