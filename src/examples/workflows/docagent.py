from ..agents import create_agent, create_doc_agent
from ..tools.tool_loader import load_and_register_tools


def run_doc(
    pdf_path: str,
    initial_query: str,
    follow_ups: list[str] | None = None,
    collection_name: str = "my_docs"
) -> dict:
    agent = create_doc_agent(collection_name=collection_name)

    # 📥 Étape 1 : Ingestion + requête initiale
    res = agent.run(message=f"Ingère {pdf_path}. {initial_query}", max_turns=2)
    print(res.process())
    answer_0 = res.summary.strip() if res.summary else "AUCUNE_RÉPONSE"

    history = [{"query": initial_query, "answer": answer_0}]

    # 🔁 Étape 2 : Questions de suivi
    if follow_ups:
        for q in follow_ups:
            res = agent.run(message=q, max_turns=2)
            history.append({"query": q, "answer": res.summary.strip() if res.summary else "AUCUNE_RÉPONSE"})

    return {"pdf_path": pdf_path, "collection_name": collection_name, "conversation": history}
