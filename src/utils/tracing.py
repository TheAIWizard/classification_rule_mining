import re
from functools import wraps
from typing import Any, Dict
from ..utils.io import langfuse
from ..utils.agent_utils import compute_agent_metrics, extract_tool_events


# 🔹 Sanitisation : on garde tout, mais on nettoie les secrets
def _sanitize_cfg(cfg: Dict[str, Any]) -> Dict[str, Any]:
    if not cfg:
        return {}
    safe = cfg.copy()

    # 🔒 Masquage ou suppression de l'api_key
    if "api_key" in safe:
        safe["api_key"] = re.sub(r"(sk-)[\w-]+", r"\1xxxx", safe["api_key"])
        # ou safe.pop("api_key") si tu préfères supprimer

    # supprimer les metadata qui polluent
    safe.pop("price", None)
    safe.pop("stream", None)
    return safe


def trace_langfuse(func):
    """
    Décorateur pour tracer automatiquement les appels d'agents.
    ⚠️ Remarque sur la modularité :
    Ce décorateur n'est pas suffisamment modulaire à l'état actuel. Il est principalement
    conçu pour le lancement de chats d'agents simples, comme les `ConversableAgent`
    AutoGen qui utilisent potentiellement des outils. Il repose sur la détection de
    `chat_history` et parse les événements d'outils après exécution.
    🔮 Évolution recommandée :
    Si votre architecture évolue vers d'autres types d'agents (GroupChat, CrewAI, etc.),
    il sera probablement nécessaire de renommer les fonctions utilitaires `_agent`
    (ex: `create_agent`) en `create_conversable_agent` afin de préserver la clarté
    sémantique et d'adapter le traçage aux nouvelles structures de messages.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Récupère dynamiquement le nom passé en argument, sinon prend le nom de la fonction
        span_name = kwargs.get("span_name", f"{func.__name__}")
        # Extraction dynamique des paramètres de configuration (ex: max_turns)
        agent_config = kwargs.get("agent")
        max_turns_config = kwargs.get("max_turns")
        summary_method_config = kwargs.get("summary_method")
        user_prompt_config = kwargs.get("user_prompt")
        # 📝 Extraction propre & sécurisée
        llm_meta = _sanitize_cfg(agent_config.llm_config._model.config_list[0].model_dump())

        # Utilisation du context manager officiel pour une gestion propre de la span [1]
        with langfuse.start_as_current_observation(
            as_type="span",
            name=span_name
        ) as span:
            try:
                span.update(input=user_prompt_config)
                # 1. Exécution du code métier
                result = func(*args, **kwargs)

                # 2. Post-traitement

                metrics = compute_agent_metrics(result.chat_history)
                tool_events = extract_tool_events(result.chat_history)

                # 3. Création des spans imbriquées pour chaque outil utilisé
                for evt in tool_events:
                    with langfuse.start_as_current_observation(
                        as_type="span",
                        name=f"tool_{evt['tool_name']}"
                    ) as tool_span:
                        output_preview = evt.get("output", "")[:8000]
                        tool_span.update(
                            input=evt.get("input"),
                            output=output_preview
                        )

                # 4. Mise à jour de la span parent avec les résultats et metadata dynamiques
                span.update(
                    output=str(result.summary)[:5000],
                    metadata={
                        "LLM_config": llm_meta,
                        "max_turns": max_turns_config,
                        "summary_method": summary_method_config,
                        "actual_turns": metrics["agent_iterations"],
                        "tool_calls_count": metrics["tool_calls_count"],
                        "conversation_rounds": metrics["conversation_rounds"]
                    }
                )

                return result
            except Exception as e:
                # Enregistrement de l'erreur dans la trace pour faciliter le débogage
                span.update(status="Error", output=str(e))
                raise
      
    return wrapper
