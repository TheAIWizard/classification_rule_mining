import os

# 🔹 Single source of truth (clés partagées)
BASE_LLM_CONFIG = {
    "api_type": "openai",
    "base_url": os.getenv("LLM_BASE_URL", "http://llm.lab.sspcloud.fr/api"),
    "api_key": os.getenv("LLM_API_KEY"),
}

# 🔹 Dérivations explicites (hérite + override du modèle uniquement)
LLM_GEMMA4_26B = {**BASE_LLM_CONFIG, "model": "gemma4-26b-moe"}
LLM_GEMMA4_31B = {**BASE_LLM_CONFIG, "model": "gemma4-31b"}
LLM_QWEN3_35B = {**BASE_LLM_CONFIG, "model": "qwen3-35b-moe"}

# 🔹 Mapping déclaratif : agent → config LLM
AGENT_MODEL_MAP = {
    "executor_agent": None,
    "date_agent":       LLM_GEMMA4_26B,
    "weather_agent":       LLM_GEMMA4_26B,
}