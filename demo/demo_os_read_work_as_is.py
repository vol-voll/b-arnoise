def lire_fichier(chemin_fichier):
    """
    Lit un fichier texte et cree une liste pour chaque ligne.

    Args:
        chemin_fichier (str): Chemin du fichier à lire.

    Returns:
        list: Liste contenant chaque ligne.
    """
    variables = []

    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()

    for i, ligne in enumerate(lignes):
        variables.append(ligne.strip())

    return variables

# Exemple d'utilisation
chemin = "PrivateKey"
variables_lues = lire_fichier(chemin)

print(variables_lues)
