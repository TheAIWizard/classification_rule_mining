from ..agents import create_agent
from ..utils.io import langfuse
from ..utils.agent_utils import extract_json
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
