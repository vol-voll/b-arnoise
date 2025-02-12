def lister_fichiers_audio(dossier):
    """
    Explore récursivement un dossier et stocke uniquement les fichiers audio trouvés,
    sans leur extension.

    Args:
        dossier (str): Chemin du dossier à explorer.

    Returns:
        list: Liste des noms de fichiers audio (sans leur extension et sans leur chemin).
    """
    from os import walk, path

    fichiers_audio = []
    music_formats = {".aiff", ".au", ".mp3", ".m4a", ".wav", ".wma", ".aac", ".ogg", ".pcm", ".caf"}

    for _, _, fichiers in walk(dossier):  
        for fichier in fichiers:
            nom_fichier, extension = path.splitext(fichier)  # Sépare le nom et l'extension
            if extension.lower() in music_formats:  # Vérifie si c'est un fichier audio
                fichiers_audio.append(nom_fichier)  # Ajoute uniquement le nom sans extension

    return fichiers_audio

# Exemple d'utilisation
chemin_de_depart = "."  # "." signifie le dossier actuel
liste_des_fichiers_audio = lister_fichiers_audio(chemin_de_depart)

# Affichage des fichiers audio trouvés
for fichier in liste_des_fichiers_audio:
    print(fichier)
