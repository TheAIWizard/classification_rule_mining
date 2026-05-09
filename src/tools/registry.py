from .tools import lookup_codes, search_naf_concepts, analyze_impact_cluster

TOOL_REGISTRY = {
    "lookup_codes": lookup_codes,
    "search_naf_concepts": search_naf_concepts,
    "analyze_impact_cluster": analyze_impact_cluster
}
