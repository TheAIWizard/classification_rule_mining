from autogen import ConversableAgent
from autogen.agents.experimental import DocAgent, InMemoryQueryEngine
from autogen.agents.experimental.document_agent.chroma_query_engine import VectorChromaCitationQueryEngine

from .config import AGENT_MODEL_MAP
from .prompts import AGENT_PROMPTS
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# 🛠️ Fix version-proof : force l'embeddings local sans clé API
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_agent(
    name: str,
    human_input_mode: str = "ALWAYS",
    llm_config: dict | None = None,
    system_message: str | None = None,
    **kwargs
) -> ConversableAgent:
    """Factory pour créer un agent AutoGen/AG2 avec prompt et modèle associés.

    Args:
        name: Nom de l'agent (doit exister dans AGENT_MODEL_MAP & AGENT_PROMPTS)
        human_input_mode: "NEVER", "ALWAYS" ou "TERMINATE"
        llm_config: Override du modèle/config LLM (si None, utilise config.py)
        system_message: Override du prompt système (si None, utilise prompts.py)
        **kwargs: Arguments supplémentaires passés à ConversableAgent 
                  (ex: is_termination_msg, max_concurrent_workers, etc.)
           
    Returns:
        ConversableAgent prêt à l'emploi
    """
    if name not in AGENT_MODEL_MAP:
        raise KeyError(
            f"Agent '{name}' inconnu. Agents disponibles: {list(AGENT_MODEL_MAP.keys())}"
        )
    print(AGENT_MODEL_MAP)
    return ConversableAgent(
        name=name,
        system_message=system_message or AGENT_PROMPTS.get(name, ""),
        llm_config=llm_config or AGENT_MODEL_MAP[name],
        human_input_mode=human_input_mode,
        **kwargs
    )


def create_doc_agent(
    collection_name: str = "default_docs",
    llm_config: dict | None = None,
    **kwargs
) -> DocAgent:
    """Factory DocAgent avec persistance vectorielle via collection_name."""
    cfg = llm_config or AGENT_MODEL_MAP.get("doc_agent")
    inmemory_qe = InMemoryQueryEngine(llm_config=cfg)
    #query_engine = VectorChromaCitationQueryEngine(collection_name=collection_name, enable_query_citations=True)
    return DocAgent(name="doc_agent", llm_config=cfg, collection_name=collection_name, query_engine=inmemory_qe, **kwargs)