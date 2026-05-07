from .utils.io import langfuse

prompt_analyste = langfuse.get_prompt("agent_analyse_naf", label="latest").prompt
prompt_auditeur = langfuse.get_prompt("agent_auditeur_naf", label="latest").prompt
prompt_juge = langfuse.get_prompt("agent_juge_naf", label="latest").prompt
prompt_expertise_batch = langfuse.get_prompt("agent_expertise_batch", label="latest").prompt
prompt_clusterer_batch = langfuse.get_prompt("agent_clusterer_batch", label="latest").prompt
prompt_clusters_merger = langfuse.get_prompt("agent_clusters_merger", label="latest").prompt
prompt_rules_impact_check = langfuse.get_prompt("agent_rules_impact_check", label="latest").prompt
prompt_rules_renderer_md = langfuse.get_prompt("agent_rules_renderer_md", label="latest").prompt

AGENT_PROMPTS = {
    "agent_analyse_naf": prompt_analyste,
    "agent_auditeur_naf": prompt_auditeur,
    "agent_juge_naf": prompt_juge,
    "agent_expertise_batch": prompt_expertise_batch,
    "agent_clusterer_batch": prompt_clusterer_batch,
    "agent_clusters_merger": prompt_clusters_merger,
    "agent_rules_impact_check": prompt_rules_impact_check,
    "agent_rules_renderer_md": prompt_rules_renderer_md,
}
