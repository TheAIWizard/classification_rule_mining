# src/utils/tracing.py
from functools import wraps
from ..utils.io import langfuse


def trace_langfuse(func):
    """
    Décorateur pour tracer automatiquement les appels d'agents.
    Capture les paramètres de configuration pour les ajouter aux metadata Langfuse.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Récupérer les paramètres d'intérêt (ex: max_turns)
        config_metadata = {
            "max_turns": kwargs.get("max_turns"),
            "summary_method": kwargs.get("summary_method")
        }

        # 2. Ouverture de la span parente (selon la documentation [1])
        with langfuse.start_as_current_observation(
            as_type="span", 
            name=f"{func.__name__}"
        ) as span:
            try:
                # 3. Exécution de l'étape agent
                result = func(*args, **kwargs)
              
                # 4. Mise à jour de la trace avec le résumé
                # Note: On suppose que le résultat a un attribut 'summary'
                if hasattr(result, 'summary'):
                    span.update(
                        output=str(result.summary)[:5000],
                        metadata=config_metadata
                    )
                else:
                    span.update(output=str(result))

                return result
            except Exception as e:
                span.update(status="Error", output=str(e))
                raise
    return wrapper
