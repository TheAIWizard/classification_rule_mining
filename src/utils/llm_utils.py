import json
import re
from typing import Any


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
