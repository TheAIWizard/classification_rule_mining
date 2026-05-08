import json
from ..agents import create_agent
from ..config import PATH
from ..utils.io import langfuse, load_data_to_dict, save_results, save_md, save_json
from ..utils.agent_utils import extract_json, extract_json_list
from ..utils.data_utils import chunk_list
from ..utils.tracing import trace_langfuse
from ..tools.tool_loader import load_and_register_tools


@trace_langfuse
def run_agent_step(agent,
                   executor,
                   user_prompt,
                   max_turns=2, summary_method="last_msg", span_name="agent_name"):
    """
    Fonction générique pour lancer une étape/interaction d'un agent à renseigner.
    Chaque appel à cette fonction sera tracé individuellement par Langfuse.
    """
    return executor.initiate_chat(
        recipient=agent,
        message=user_prompt,
        max_turns=max_turns,
        summary_method=summary_method
    )


def run_extract_rules(libellé="coiffeur ambulant",
                      code_proposé="9621H",
                      code_observé="9621G") -> dict:
    """Pipeline séquentiel : feedback → agents → rules."""

    # 1️⃣ Setup
    agent_analyse_naf = create_agent("agent_analyse_naf", human_input_mode="NEVER")
    agent_auditeur_naf = create_agent("agent_auditeur_naf", human_input_mode="NEVER")
    agent_juge_naf = create_agent("agent_juge_naf", human_input_mode="NEVER")

    executor = create_agent("executor_agent", human_input_mode="NEVER")

    # 🧰 Outillage
    load_and_register_tools(["lookup_codes"], agent_analyse_naf, executor)
    load_and_register_tools(["lookup_codes"], agent_auditeur_naf, executor)

    # 2️⃣ Analyse

    user_prompt_analyse = f"""📥 CONSIGNE ANALYSE
────────────────────
Libellé : {libellé}
Codes soumis : [{code_proposé}, {code_observé}]
────────────────────
Rends-toi strictement dans le format demandé dans ton prompt système.
"""

    res_analyse = run_agent_step(agent=agent_analyse_naf,
                                 executor=executor,
                                 user_prompt=user_prompt_analyse,
                                 span_name="agent_analyse_naf")
    res_analyse_text = res_analyse.summary.strip()

    # 3️⃣ Audit

    user_prompt_audit = f"""📥 CONSIGNE AUDIT
────────────────────
Texte à objectiver :
{res_analyse_text}
────────────────────
Rends-toi dans le format de ton prompt système.
"""

    res_audit = run_agent_step(agent=agent_auditeur_naf,
                               executor=executor,
                               user_prompt=user_prompt_audit,
                               span_name="agent_auditeur_naf")
    res_audit_text = res_audit.summary.strip()

    # 4️⃣ Arbitrage

    user_prompt_juge = (
        f"📥 CONTEXTE D'ENTRÉE\n"
        f"<analyse_experte>\n{res_analyse_text}\n</analyse_experte>\n\n"
        f"<rapport_audit>\n{res_audit_text}\n</rapport_audit>\n\n"
    )

    res_juge = run_agent_step(agent=agent_juge_naf,
                              executor=executor,
                              user_prompt=user_prompt_juge,
                              span_name="agent_juge_naf")
    res_juge_text = res_juge.summary.strip()

    res_juge_json = extract_json(res_juge_text)

    # Flush obligatoire en fin de pipeline court pour garantir l'envoi des traces [1]
    langfuse.flush()

    return res_juge_json


def run_extract_rules_batch(chunck_size=50) -> dict:
    """Pipeline séquentiel : feedback → agents → rules."""

    # 1️⃣ Setup

    agent_expertise_batch = create_agent("agent_expertise_batch", human_input_mode="NEVER")
    agent_clusterer_batch = create_agent("agent_clusterer_batch", human_input_mode="NEVER")
    agent_clusters_merger = create_agent("agent_clusters_merger", human_input_mode="NEVER")
    agent_rules_impact_check = create_agent("agent_rules_impact_check", human_input_mode="NEVER")
    agent_rules_renderer_md = create_agent("agent_rules_renderer_md", human_input_mode="NEVER")

    executor = create_agent("executor_agent", human_input_mode="NEVER")

    feedback_data = load_data_to_dict(PATH["INPUT"])
    feedback_data_list = chunk_list(feedback_data, chunk_size=chunck_size)

    res_expertise_json_list = []

    for chunk in feedback_data_list:
        res_expertise = run_agent_step(agent=agent_expertise_batch,
                                       executor=executor,
                                       user_prompt=f"DONNÉES À TRAITER :\n{json.dumps(chunk, ensure_ascii=False, indent=2)}\n",
                                       span_name="agent_expertise_batch")
        res_expertise_text = res_expertise.summary.strip()
        res_expertise_json = extract_json_list(res_expertise_text)
        res_expertise_json_list += res_expertise_json
    save_json(res_expertise_json, f"{PATH['OUTPUT']}/expertise")
    save_results(res_expertise_json_list, PATH["OUTPUT"])

    res_clusters_json_list = []

    chuncked_res_expertise_json_list = chunk_list(res_expertise_json_list, chunk_size=chunck_size)
    for chunk in chuncked_res_expertise_json_list:
        res_clusters = run_agent_step(agent=agent_clusterer_batch,
                                      executor=executor,
                                      user_prompt=f"DONNÉES À TRAITER :\n{json.dumps(chunk, ensure_ascii=False, indent=2)}\n",
                                      span_name="agent_clusterer_batch")
        res_clusters_text = res_clusters.summary.strip()
        res_clusters_json = extract_json_list(res_clusters_text)
        res_clusters_json_list += res_clusters_json
    save_json(res_clusters_json, f"{PATH['OUTPUT']}/clusters")
    save_results(res_clusters_json_list, PATH["OUTPUT"])

    res_clusters_merger = run_agent_step(agent=agent_clusters_merger,
                                         executor=executor,
                                         user_prompt=str(res_clusters_json_list),
                                         span_name="agent_clusters_merger")
    res_clusters_merger_text = res_clusters_merger.summary.strip()
    res_clusters_merger_json = extract_json_list(res_clusters_merger_text)
    save_json(res_clusters_merger_json, f"{PATH['OUTPUT']}/clusters_merge")
    save_results(res_clusters_merger, PATH["OUTPUT"])

    res_rules_impact_check = run_agent_step(agent=agent_rules_impact_check,
                                            executor=executor,
                                            user_prompt=res_clusters_merger_text,
                                            span_name="agent_rules_impact_check")
    res_rules_impact_check_text = res_rules_impact_check.summary.strip()

    save_results(res_rules_impact_check_text, PATH["OUTPUT"])

    res_rules_renderer_md = run_agent_step(agent=agent_rules_renderer_md,
                                           executor=executor,
                                           user_prompt=res_rules_impact_check_text,
                                           span_name="agent_rules_renderer_md")
    res_rules_renderer_md_text = res_rules_renderer_md.summary.strip()
    save_md(res_rules_renderer_md_text, PATH["OUTPUT"])
