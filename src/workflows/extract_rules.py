from ..agents import create_agent
from ..utils.llm_utils import extract_json
# from ..tools.tool_loader import load_and_register_tools


def run_extract_rules(libellé="Je suis créateur de contenu, vidéaste."
                              "Je fais des vidéos youtube et fais de la publicité "
                              "pour des marques qui me proposent des partenariats",
                      code_proposé="5911G",
                      code_observé="5911H") -> dict:
    """Pipeline séquentiel : feedback → agents → rules."""

    # 1️⃣ Setup
    agent_analyse_naf = create_agent("agent_analyse_naf", human_input_mode="NEVER")
    agent_auditeur_naf = create_agent("agent_auditeur_naf", human_input_mode="NEVER")
    agent_juge_naf = create_agent("agent_juge_naf", human_input_mode="NEVER")

    executor = create_agent("executor_agent", human_input_mode="NEVER")

    # 2️⃣ Registration par scope
    # load_and_register_tools(["get_naf_notes"], date_agent, executor)
    # load_and_register_tools(["get_weather"], weather_agent, executor)

    # 2️⃣ Analyse
    res_analyse = executor.initiate_chat(
        recipient=agent_analyse_naf,
        message=f"""📥 CONSIGNE ANALYSE
────────────────────
Libellé : {libellé}
Codes soumis : [{code_proposé}, {code_observé}]
────────────────────
Rends-toi strictement dans le format demandé dans ton prompt système.
""",
        max_turns=1,
        summary_method="last_msg"  # "reflection_with_llm" => resume history with llm
    )
    res_analyse = res_analyse.summary.strip()

    # 3️⃣ Audit
    res_audit = executor.initiate_chat(
        recipient=agent_auditeur_naf,
        message=f"""📥 CONSIGNE AUDIT
────────────────────
Texte à objectiver :
{res_analyse}
────────────────────
Rends-toi dans le format de ton prompt système.
""",
        max_turns=1,
        summary_method="last_msg"  # "reflection_with_llm" => resume history with llm
    )
    res_audit = res_audit.summary.strip()

    # 4️⃣ Arbitrage
    res_juge = executor.initiate_chat(
        recipient=agent_juge_naf,
        message=f"📥 CONTEXTE D'ENTRÉE\n"
                f"<analyse_sous>\n{res_analyse}\n</analyse_sous>\n\n"
                f"<audit_sous>\n{res_audit}\n</audit_sous>\n\n",
        max_turns=1,
        summary_method="last_msg"  # "reflection_with_llm" => resume history with llm
    )
    res_juge = res_juge.summary.strip()
    res_juge_json = extract_json(res_juge)

    return res_juge_json
