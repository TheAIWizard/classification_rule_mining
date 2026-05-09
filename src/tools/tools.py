import re
import json
from typing import Annotated, List
from qdrant_client.http.models import Filter, FieldCondition, MatchText
from ..utils.io import get_qdrant_client, get_duckdb_connection
from ..utils.data_utils import normalize_ape
from ..utils.embeddings import get_embedding


_CODE_RE = re.compile(r"^\d{2}\.\d{2}[A-Z]$")


def lookup_codes(codes: Annotated[List[str], "Liste de codes NAF/APE"]) -> str:
    # 1️⃣ Filtrer : on garde uniquement les codes valides, les autres sont ignorés (à paramétriser)
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


def search_naf_concepts(query: str) -> str:
    client = get_qdrant_client()

    # On transforme la requête textuelle en vecteur de 1024 dim
    query_vector = get_embedding(query)

    search_result, _ = client.search(
        collection_name="labels_embeddings",
        query_vector=query_vector,
        limit=5
    )


def analyze_impact_cluster(
    s3_path: str,
    column_name: str,
    search_term: str,
    recommended_ape: str,
    sample_size: int = 5
):
    """
    Analyse un cluster NAF à partir d'un terme métier et retourne des statistiques agrégées.

    Cette fonction interroge une base parquet via DuckDB en appliquant un filtre textuel
    sur une colonne donnée, puis calcule des métriques de qualité de classification NAF.

    Elle ne retourne jamais de données brutes, uniquement des agrégats nécessaires
    à l'évaluation d'un cluster métier.

    Paramètres
    ----------
    s3_path : str
        Chemin S3 du fichier parquet contenant les données NAF.
    column_name : str
        Nom de la colonne textuelle utilisée pour la recherche (ex: libelle_analyse).
    search_term : str
        Terme métier utilisé pour filtrer les lignes (doit être court et spécifique).
    recommended_ape : str
        Code APE de référence utilisé pour évaluer la correction.

    Retour
    ------
    dict
        Dictionnaire contenant :

        - search_term : terme utilisé pour la recherche
        - volume_total_match : nombre total de lignes correspondantes
        - volume_deja_correct : lignes déjà associées au bon code APE
        - volume_a_corriger : lignes associées à un mauvais code APE
        - taux_correction : proportion de mauvais classement
        - top_ape_observes : distribution des codes APE dominants
        - samples_bruit : exemples représentatifs de cas hors cible

    Notes
    -----
    - La fonction effectue toute l'agrégation côté SQL (DuckDB).
    - Aucun post-traitement de volume ne doit être fait par l'appelant.
    - Les résultats sont conçus pour alimenter un agent de décision, pas une analyse brute.
    """
    con = get_duckdb_connection()

    try:
        recommended_ape = normalize_ape(recommended_ape)
        query = f"""
        WITH matches AS (
            SELECT
                nace2025,
                {column_name} AS label
            FROM read_parquet('{s3_path}')
            WHERE {column_name} ILIKE ?
        )

        SELECT
            COUNT(*) AS volume_total_match,

            COUNT(*) FILTER (
                WHERE nace2025 = ?
            ) AS volume_deja_correct,

            COUNT(*) FILTER (
                WHERE nace2025 != ?
            ) AS volume_a_corriger

        FROM matches
        """

        stats = con.execute(
            query,
            [f"%{search_term}%", recommended_ape, recommended_ape]
        ).fetchone()

        top_ape_query = f"""
        SELECT
            nace2025,
            COUNT(*) AS count
        FROM read_parquet('{s3_path}')
        WHERE {column_name} ILIKE ?
        GROUP BY nace2025
        ORDER BY count DESC
        LIMIT 5
        """

        top_apes = con.execute(
            top_ape_query,
            [f"%{search_term}%"]
        ).fetchall()

        bruit_query = f"""
        SELECT {column_name}
        FROM read_parquet('{s3_path}')
        WHERE {column_name} ILIKE ?
        AND nace2025 != ?
        LIMIT ?
        """

        bruit = con.execute(
            bruit_query,
            [f"%{search_term}%", recommended_ape, sample_size]
        ).fetchall()

        total, correct, incorrect = stats

        return {
            "search_term": search_term,
            "volume_total_match": total,
            "volume_deja_correct": correct,
            "volume_a_corriger": incorrect,
            "taux_correction":
                incorrect / total if total else 0,
            "top_ape_observes": [
                {"ape": r[0], "count": r[1]}
                for r in top_apes
            ],
            "samples_bruit": [r[0] for r in bruit]
        }

    finally:
        con.close()
