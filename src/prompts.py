from .utils.io import langfuse

prompt_analyste = langfuse.get_prompt("agent_analyse_naf", label="latest").prompt
prompt_auditeur = langfuse.get_prompt("agent_auditeur_naf", label="latest").prompt
prompt_juge = langfuse.get_prompt("agent_juge_naf", label="latest").prompt

AGENT_PROMPTS = {
    "agent_analyse_naf": prompt_analyste,
    "agent_auditeur_naf": prompt_auditeur,
    "agent_juge_naf": prompt_juge,
}
