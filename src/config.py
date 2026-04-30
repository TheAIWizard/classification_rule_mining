import os

# Config LLM de base (peut être écrasée par AGENT_MODEL_MAP)
BASE_LLM_CONFIG = {
    "api_type": "openai",
    "model": os.getenv("LLM_MODEL", "gemma4-26b-moe"),
    "base_url": os.getenv("LLM_LAB_BASE_URL"),
    "api_key": os.getenv("LLM_API_KEY"),
}

# Mapping simple : nom_agent → config LLM spécifique
# → Tu peux changer le modèle de n'importe quel agent ici
AGENT_MODEL_MAP = {
    "date_agent": BASE_LLM_CONFIG,
    "executor_agent": BASE_LLM_CONFIG,
    "judge_agent": {
        "api_type": "openai",
        "model": os.getenv("JUDGE_MODEL", "qwen3-35b-moe"),
        "base_url": os.getenv("LLM_BASE_URL"),
        "api_key": os.getenv("LLM_API_KEY"),
    }
}