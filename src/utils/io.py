import os
import json
import pandas as pd
import s3fs
import duckdb
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from langfuse import get_client

langfuse = get_client()


def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns the Qdrant client.
    """
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        port=443,
        https=True,
    )


def is_s3_path(path: str) -> bool:
    """Check if the path points to S3."""
    return path.startswith("s3://")


def get_filesystem() -> s3fs.S3FileSystem:
    """
    Configure and return a S3-compatible filesystem (MinIO / AWS S3).
    Uses environment variables for configuration.
    """
    return s3fs.S3FileSystem(
        client_kwargs={
            "endpoint_url": os.environ.get("AWS_S3_ENDPOINT")
        },
        key=os.environ.get("AWS_ACCESS_KEY_ID"),
        secret=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_duckdb_connection():
    """
    Configure et retourne une connexion DuckDB prête pour S3.
    Initialise l'extension httpfs indispensable pour lire sur S3.
    """
    con = duckdb.connect(database=':memory:')
    con.execute("INSTALL httpfs; LOAD httpfs;")

    # Configuration des credentials S3 dans DuckDB
    endpoint = os.environ.get("AWS_S3_ENDPOINT")
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if endpoint:
        con.execute(f"SET s3_endpoint='{endpoint}';")
        con.execute("SET s3_url_style='path';")  # Nécessaire pour MinIO

    con.execute(f"SET s3_access_key_id='{access_key}';")
    con.execute(f"SET s3_secret_access_key='{secret_key}';")

    return con


# --- CHARGEMENT ET TRANSFORMATION ---
def load_data_to_dict(path: str, file_type: str = "csv") -> List[Dict]:
    """
    Load CSV or ODS from local or S3 and return as a list of dictionaries.

    Args:
        path (str): Local path or S3 path (e.g., 's3://bucket/file.csv')
        file_type (str): 'csv' or 'ods'
     
    Returns:
        List[Dict]: Cleaned list of dictionaries.
    """
  
    # 1. Chargement du DataFrame
    if is_s3_path(path):
        fs = get_filesystem()
        with fs.open(path, mode="rb") as f:
            if file_type.lower() == "csv":
                df = pd.read_csv(f)
            elif file_type.lower() == "ods":
                df = pd.read_excel(f, engine='odf')
            else:
                raise ValueError(f"Format {file_type} non supporté.")
    else:
        # Chargement Local
        if file_type.lower() == "csv":
            df = pd.read_csv(path)
        elif file_type.lower() == "ods":
            df = pd.read_excel(path, engine='odf')
        else:
            raise ValueError(f"Format {file_type} non supporté.")

    # 2. Nettoyage "Agent-Ready" (Crucial pour éviter les erreurs de prompt)
    # - Supprime les colonnes totalement vides
    # - Remplace les NaN par des chaînes vides (évite les erreurs JSON/Prompt)
    # - Strip les espaces et sauts de ligne invisibles dans les cellules
 
    df = df.dropna(how='all', axis=1)
    df = df.fillna("")

    for col in df.select_dtypes(['object']):
        df[col] = df[col].apply(lambda x: str(x).strip() if isinstance(x, str) else x)

    # 3. Conversion en liste de dictionnaires
    return df.to_dict(orient='records')


# ... (vos fonctions existantes load_data_to_dict, is_s3_path, etc.)

def save_results(data: List[Dict], filename: str, output_dir: str = "outputs") -> str:
    """
    Sauvegarde une liste de dictionnaires dans un fichier CSV dans un dossier spécifique.
    Crée le dossier s'il n'existe pas.

    Args:
        data (List[Dict]): La liste des résultats (venant de l'agent).
        filename (str): Le nom du fichier (ex: 'batch_1_results.csv').
        output_dir (str): Le dossier de destination (par défaut 'outputs').

    Returns:
        str: Le chemin complet du fichier sauvegardé.
    """
    try:
        # 1. Création du dossier s'il n'existe pas
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Dossier créé : {output_dir}")

        # 2. Préparation du nom de fichier avec un timestamp pour éviter les écrasements accidentels
        # On peut l'ajouter ou non selon votre besoin, ici je l'ajoute pour la sécurité
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   
        # On sépare le nom et l'extension pour insérer le timestamp au milieu
        name, ext = os.path.splitext(filename)
        if not ext:
            ext = ".csv"  # Sécurité si l'utilisateur oublie l'extension
  
        final_filename = f"{name}_{timestamp}{ext}"
        full_path = os.path.join(output_dir, final_filename)

        # 3. Conversion et Sauvegarde
        df = pd.DataFrame(data)
        df.to_csv(full_path, index=False, encoding='utf-8-sig')  # compatibilité Excel

        print(f"✅ Résultats sauvegardés avec succès : {full_path}")
        return full_path

    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {str(e)}")
        raise


def save_md(content: str, file_path: str) -> None:
    """
    Enregistre un contenu string dans un fichier .md.
    ✅ Crée automatiquement les répertoires manquants
    ✅ Ajoute l'extension .md si absente
    ✅ Utilise l'encodage UTF-8 (standard Markdown)
    """
    path = Path(file_path)
    if not path.suffix:
        path = path.with_suffix(".md")
   
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def save_json(data: Any, file_path: str, default_ext: str = ".json") -> str:
    """
    Sauvegarde des données JSON avec :
    ✅ Création automatique du dossier parent
    ✅ Ajout d'un timestamp pour éviter les écrasements
    ✅ Gestion automatique de l'extension (.json par défaut)
    ✅ Encodage UTF-8 + indentation lisible
    """
    try:
        # 1. Normalisation de l'extension
        path = Path(file_path)
        if not path.suffix:
            path = path.with_suffix(default_ext)

        # 2. Insertion du timestamp avant l'extension
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path(f"{path.stem}_{timestamp}{path.suffix}")

        # 3. Création du dossier si absent
        path.parent.mkdir(parents=True, exist_ok=True)

        # 4. Sérialisation & écriture
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        
        print(f"✅ Fichier sauvegardé : {path}")
        return str(path)

    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        raise