from ..agents import create_agent
from ..utils.agent_utils import extract_json, extract_tool_events, compute_agent_metrics
from ..utils.io import langfuse
from ..tools.tool_loader import load_and_register_tools


def run_extract_rules(libellé="Je suis créateur de contenu, vidéaste"
                              "Je fais parfois des vidéos youtube et fais de la publicité "
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

    with langfuse.start_as_current_observation(as_type="span",
                                               name="agent_analyse_naf") as span_analyse:
        # Tracer l'input
        span_analyse.update(input=user_prompt_analyse)

        res_analyse = executor.initiate_chat(
                recipient=agent_analyse_naf,
                message=user_prompt_analyse,
                max_turns=2,
                summary_method="last_msg"  # "reflection_with_llm" => resume history with llm
        )

        # 3. Extraction propre évènements appel outils depuis chat_history + métriques
        tool_events = extract_tool_events(res_analyse.chat_history)
        metrics = compute_agent_metrics(res_analyse.chat_history)

        # 4. Spans imbriqués pour chaque outil appelé
        for evt in tool_events:
            with langfuse.start_as_current_observation(
                as_type="span",
                name=f"tool_{evt['tool_name']}"
            ) as tool_span:
                # Troncature intelligente pour éviter la saturation UI
                output_preview = evt.get("output", "")[:8000]
                tool_span.update(
                    input=evt["input"],
                    output=output_preview
                )

        span_analyse.update(
            # input={"libellé": libellé, "code_proposé": code_proposé},
            output=res_analyse.summary.strip(),
            metadata={"max_turns": 2,
                      "actual_turns": metrics["agent_iterations"],
                      "tool_calls_count": metrics["tool_calls_count"],
                      "conversation_rounds": metrics["conversation_rounds"],
                      "chat_history": res_analyse}
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
        max_turns=2,
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
    print(res_juge)
    res_juge_json = extract_json(res_juge)

    return res_juge_json
