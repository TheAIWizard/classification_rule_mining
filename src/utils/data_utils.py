def chunk_list(data: list, chunk_size: int) -> list[list]:
    """
    Découpe une liste en plusieurs sous-listes de taille donnée.
    """
    return [data[i: i + chunk_size] for i in range(0, len(data), chunk_size)]
