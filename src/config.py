import os

# 🔹 Single source of truth (clés partagées)
BASE_LLM_CONFIG = {
    "api_type": "openai",
    "base_url": os.getenv("LLM_LAB_BASE_URL"),
    "api_key": os.getenv("LLM_LAB_API_KEY"),
    "price": [0.00008, 0.00028]
}

# 🔹 Dérivations explicites (hérite + override du modèle uniquement)
LLM_GEMMA4_26B = {**BASE_LLM_CONFIG, "model": "gemma4-26b-moe"}
LLM_GEMMA4_31B = {**BASE_LLM_CONFIG, "model": "gemma4-31b"}
LLM_QWEN3_6_35B = {**BASE_LLM_CONFIG, "model": "qwen3-6-35b-moe"}

# 🔹 Mapping déclaratif : agent → config LLM
AGENT_MODEL_MAP = {
    "executor_agent": None,
    "agent_analyse_naf":       LLM_GEMMA4_26B,
    "agent_auditeur_naf":       LLM_GEMMA4_26B,
    "agent_juge_naf":       LLM_GEMMA4_26B,
    "agent_expertise_batch":       LLM_GEMMA4_26B,
    "agent_clusterer_batch":       LLM_GEMMA4_26B,
}

PATH = {
    "INPUT": "./inputs/feedback_data.csv",
    "OUTPUT": "./outputs",
}
