import json
import re
from typing import List, Dict, Any


def extract_json(text: str) -> dict[str, Any]:
    """Extrait & parse un JSON pur depuis la sortie d'un LLM.
    Gère les ```json, les guillemets internes cassés, et les espaces parasites.
    """
    # Nettoyage des éventuels blocs markdown
    clean = re.sub(r'```(?:json)?\s*', '', text).strip()

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass

    # Fallback : répare les guillemets non échappés à l'intérieur des strings
    # Ex: `"texte "mot" texte"` -> `"texte \"mot\" texte"`
    fixed = re.sub(r'(?<=\s)(?<!:\s)"(?=\w)', r'\"', clean)

    try:
        return json.loads(fixed)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ JSON parse échoué: {e}\n>>> {text[:200]}")


def extract_json_list(text: str) -> List[Dict[str, Any]]:
    """
    Extrait une liste JSON depuis une sortie LLM robuste.

    Gère :
    - texte avant/après
    - markdown ```json
    - objet unique ou liste
    - plusieurs blocs JSON
    - espaces parasites

    Retour :
    - list[dict]
    """

    if not text or not text.strip():
        return []

    # ---------------------------------------------------------
    # 1. Nettoyage markdown
    # ---------------------------------------------------------

    clean = text.strip()

    clean = re.sub(
        r"```(?:json)?",
        "",
        clean,
        flags=re.IGNORECASE
    )

    clean = clean.replace("```", "").strip()

    # ---------------------------------------------------------
    # 2. Parsing direct
    # ---------------------------------------------------------

    try:
        data = json.loads(clean)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return [data]

    except Exception:
        pass

    # ---------------------------------------------------------
    # 3. Recherche d'une liste JSON
    # ---------------------------------------------------------

    start = clean.find("[")
    end = clean.rfind("]")

    if start != -1 and end != -1 and end > start:

        candidate = clean[start:end + 1]

        try:
            data = json.loads(candidate)

            if isinstance(data, list):
                return data

        except Exception:
            pass

    # ---------------------------------------------------------
    # 4. Recherche d'un objet JSON
    # ---------------------------------------------------------

    start = clean.find("{")
    end = clean.rfind("}")

    if start != -1 and end != -1 and end > start:

        candidate = clean[start:end + 1]

        try:
            data = json.loads(candidate)

            if isinstance(data, dict):
                return [data]

        except Exception:
            pass

    # ---------------------------------------------------------
    # 5. Tentative avancée :
    #    extraction de plusieurs objets JSON concaténés
    # ---------------------------------------------------------

    objects = re.findall(
        r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}",
        clean,
        flags=re.DOTALL
    )

    parsed = []

    for obj in objects:

        try:
            data = json.loads(obj)

            if isinstance(data, dict):
                parsed.append(data)

        except Exception:
            continue

    if parsed:
        return parsed

    # ---------------------------------------------------------
    # 6. Échec final
    # ---------------------------------------------------------

    print("❌ Impossible d'extraire du JSON")
    print(clean[:1000])

    return []


def extract_tool_events(chat_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parse la structure native AG2 pour associer appels d'outils et réponses.
    Ignore le chat_history brut et retourne uniquement les événements utiles.
    """
    events = []
    pending_tool = None

    for msg in chat_history:
        role = msg.get("role")

        # Détection de la demande d'outil (assistant)
        if role == "assistant" and "tool_calls" in msg:
            for tc in msg["tool_calls"]:
                pending_tool = {
                    "call_id": tc.get("id"),
                    "tool_name": tc["function"]["name"],
                    "input": tc["function"].get("arguments", {}),
                    "output": None
                }

        # Associe la réponse de l'outil à la demande en attente
        elif role == "tool" and "tool_responses" in msg and pending_tool:
            for resp in msg["tool_responses"]:
                if resp.get("tool_call_id") == pending_tool["call_id"]:
                    pending_tool["output"] = resp.get("content", "")
                    events.append(pending_tool)
                    pending_tool = None
    return events


def compute_agent_metrics(chat_history: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Calcule les métriques d'itération agent sans hypothèse fixe sur le nombre d'outils.
    """
    assistant_messages = [m for m in chat_history if m.get("role") == "assistant"]
    tool_calls = [
        tc
        for m in assistant_messages
        for tc in m.get("tool_calls", [])
    ]

    # 1. Nombre d'appels LLM / décisions agent (le plus fiable pour "actual_turns")
    agent_iterations = len(assistant_messages)

    # 2. Nombre total de cycles conversationnels (user/assistant pairs)
    user_or_assistant = sum(1 for m in chat_history if m.get("role") in ("user", "assistant"))
    conversation_rounds = (user_or_assistant + 1) // 2  # Arrondi supérieur pour le premier message

    return {
        "agent_iterations": agent_iterations,      # ✅ Recommandé pour actual_turns
        "llm_calls": agent_iterations,
        "tool_calls_count": len(tool_calls),
        "conversation_rounds": conversation_rounds,
        "total_messages": len(chat_history)
    }
