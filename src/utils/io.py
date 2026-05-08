import os
import json
import pandas as pd
import s3fs
import duckdb
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Union
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
    """Connexion DuckDB optimisée pour MinIO / SSPCloud."""

    con = duckdb.connect(database=":memory:")
    con.execute(
        f"""
    CREATE SECRET secret_ls3 (
        TYPE S3,
        KEY_ID '{os.environ["AWS_ACCESS_KEY_ID"]}',
        SECRET '{os.environ["AWS_SECRET_ACCESS_KEY"]}',
        ENDPOINT '{os.environ["AWS_S3_ENDPOINT"]}',
        SESSION_TOKEN '',
        REGION 'us-east-1',
        URL_STYLE 'path',
        SCOPE 's3://'
    );
    """
    )
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


def load_json(file_path: Union[str, Path], default: Any = None) -> Any:
    """
    Lit et parse un fichier JSON.
    ✅ Gère les chemins relatifs/absents
    ✅ Retourne une valeur par défaut si fichier manquant ou vide
    ✅ Erreurs explicites pour JSON corrompu
    ✅ Encodage UTF-8 garanti
    """
    path = Path(file_path)

    # Fichier inexistant → retourne default ou {}
    if not path.exists():
        return default if default is not None else {}

    try:
        # Lecture + nettoyage des espaces/retours à la ligne
        content = path.read_text(encoding="utf-8").strip()
        
        # Fichier vide → retourne default ou {}
        if not content:
            return default if default is not None else {}
            
        return json.loads(content)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"⚠️ JSON invalide dans {path} : {e}")
    except Exception as e:
        raise RuntimeError(f"❌ Erreur de lecture de {path} : {e}")


def load_json_list(file_path: Union[str, Path], default: list = None) -> list:
    """
    Lit et parse un fichier JSON contenant une liste de dictionnaires.
    ✅ Retourne [] si fichier manquant ou vide
    ✅ Wrap automatiquement un dict unique en liste [dict]
    ✅ Erreurs explicites pour JSON corrompu ou type incompatible
    ✅ Encodage UTF-8 garanti
    """
    if default is None:
        default = []

    path = Path(file_path)
    if not path.exists():
        return default

    try:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            return default

        data = json.loads(content)

        # 🔄 UX friendly : si un dict unique a été enregistré, on le transforme en liste
        if isinstance(data, dict):
            return [data]
        
        if not isinstance(data, list):
            raise ValueError(f"⚠️ Attendait une liste, trouvé : {type(data).__name__}")
            
        return data

    except json.JSONDecodeError as e:
        raise ValueError(f"❌ JSON invalide dans {path} : {e}")
    except Exception as e:
        raise RuntimeError(f"❌ Erreur lecture {path} : {e}")