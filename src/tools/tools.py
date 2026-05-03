import re
from typing import Annotated, List
from qdrant_client.http.models import Filter, FieldCondition, MatchText
from ..utils.io import get_qdrant_client


_CODE_RE = re.compile(r"^\d{2}\.\d{2}[A-Z]$")


def lookup_codes(codes: Annotated[List[str], "Liste de codes NAF/APE"]) -> str:
    valid = {c.strip().upper() for c in codes if _CODE_RE.match(c.strip())}
    if not valid:
        return "⚠️ Format attendu : XX.XXXY (ex: 62.10Y)"

    client = get_qdrant_client()
    seen_ids = set()
    unique_points = []
    for code in valid:
        # 🔍 Tuple (points, next_offset)
        points, _ = client.scroll(
            collection_name="labels_embeddings",
            scroll_filter=Filter(must=[
                FieldCondition(key="metadata.code", match=MatchText(text=code))
            ]),
            limit=5
        )

        for p in points:
            pid = str(p.id)  # ✅ Stringify pour garantir la hashabilité
            if pid not in seen_ids:
                seen_ids.add(pid)
                # p.payload est un dict natif, safe pour stockage
                unique_points.append((code, p.payload))

    if not unique_points:
        return "🔍 Aucun résultat trouvé."

    # 📝 Formatage LLM
    out = []
    for code, payload in sorted(unique_points, key=lambda x: x[0]):
        meta = payload.get("metadata", payload)
        out.append(f"### {code} : {meta.get('label', meta.get('page_content', 'N/A'))}")
        for key in ("include", "not_include", "notes"):
            val = meta.get(key, "")
            if val and str(val).strip():
                out.append(f"**{key.replace('_', ' ').title()} :**\n{val}")
        out.append("")
    return "\n".join(out)
