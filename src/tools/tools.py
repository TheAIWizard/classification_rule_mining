import re
import json
from typing import Annotated, List
from qdrant_client.http.models import Filter, FieldCondition, MatchText
from ..utils.io import get_qdrant_client


_CODE_RE = re.compile(r"^\d{2}\.\d{2}[A-Z]$")


def lookup_codes(codes: Annotated[List[str], "Liste de codes NAF/APE"]) -> str:
    # 1️⃣ Filtrer : on garde uniquement les codes valides, les autres sont ignorés
    valid = [c.strip().upper() for c in codes if _CODE_RE.match(c.strip())]

    client = get_qdrant_client()
    seen_ids = set()
    results = []

    for code in valid:
        points, _ = client.scroll(
            collection_name="labels_embeddings",
            scroll_filter=Filter(must=[
                FieldCondition(key="page_content", match=MatchText(text=code))
            ]),
            limit=5
        )
        for p in points:
            pid = str(p.id)
            if pid not in seen_ids:
                seen_ids.add(pid)
                meta = p.payload.get("metadata", {})
                if isinstance(meta, dict):
                    results.append({
                        "code": meta.get("code"),
                        "label": meta.get("label"),
                        "include": meta.get("include", ""),
                        "not_include": meta.get("not_include", ""),
                        "notes": meta.get("notes", "")
                    })

    # 2️⃣ Tri linéaire par code NAF
    results.sort(key=lambda x: x.get("code", ""))

    # 3️⃣ Retour JSON strict
    return json.dumps(results, ensure_ascii=False)
