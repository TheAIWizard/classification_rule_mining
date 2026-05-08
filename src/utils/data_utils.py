def chunk_list(data: list, chunk_size: int) -> list[list]:
    """
    Découpe une liste en plusieurs sous-listes de taille donnée.
    """
    return [data[i: i + chunk_size] for i in range(0, len(data), chunk_size)]


def normalize_ape(code: str, mode: str = "remove_dot") -> str:
    """
    Normalise ou formate un code APE selon le mode choisi.

    Parameters
    ----------
    code : str
        Code APE à transformer.
    mode : str
        - "remove_dot" : supprime le point après les 2 premiers caractères
        - "add_dot"    : ajoute un point après les 2 premiers caractères si absent

    Returns
    -------
    str
        Code APE transformé selon le mode.
    """

    if not code:
        return code

    # 🔧 MODE 1 : suppression du point (canonicalisation machine)
    if mode == "remove_dot":
        return code.replace(".", "")

    # 🔧 MODE 2 : ajout du point (format lisible métier)
    if mode == "add_dot":
        # si déjà formaté correctement
        if len(code) > 2 and code[2] == ".":
            return code
        # sinon insertion après 2 caractères
        return code[:2] + "." + code[2:]

    # fallback sécurité
    return code