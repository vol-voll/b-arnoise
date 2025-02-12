from weird_shenanigan import logo
logo=logo()
print(logo)

def ecrire_fichier(folder_path, file_name, text):
    from os import path
    if not path.exists(folder_path):
        print("The specified directory does not exist.")
    else:
        full_file_path = path.join(folder_path, file_name)

        if path.exists(full_file_path):
            file = open(full_file_path, 'a')
        else:
            file = open(full_file_path, 'w')

        file.write(text)
        file.close()


def lire_fichier(chemin_fichier,coupe):
    """
    Lit un fichier texte et cree une liste pour chaque ligne.

    Args:
        chemin_fichier (str): Chemin du fichier à lire.
        coupe (str): Entre quelle caractaire couper "" <=> "\n" 

    Returns:
        list: Liste contenant chaque ligne.
    """
    variables = []

    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()

    for i, ligne in enumerate(lignes):
        variables.append(ligne.strip())

    return variables


def tous_les_noms_d_une_playlist(URL):
    """
    Récupère la liste des titres d'une playlist Spotify à partir de son URL.

    Args :
        URL (str) : L'identifiant unique de la liste de lecture Spotify.

    Retourne :
        liste : Une liste de pistes, où chaque piste est représentée comme une liste contenant :
            - le nom de la piste (str)
            - La durée de la piste en millisecondes (int)
            - Nom de l'artiste principal (str)
            - URL de l'image de la pochette de l'album (str)
        
        Retourne None si l'URL n'est pas valide ou si une erreur survient lors de la récupération de la liste de lecture.

    Erreurs :
        - Imprime un message d'erreur et renvoie None si le format de l'URL est incorrect.
        - Imprime un message d'erreur et renvoie None si un problème survient lors de la récupération de la liste de lecture à partir de l'API Spotify.
    """
    try:
        Key = lire_fichier("PrivateKey","")
        client_id,client_secret,redirect_uri = Key[0],Key[1],Key[2]
    except:
        client_id,client_secret = "",""
        while len(client_id) != 32:
            client_id = input("Insérer votre \"Client ID\" (vous le trouverez à l'adresse https://developer.spotify.com/) : ")
        while len(client_secret) != 32:
            client_secret = input("Insérer votre \"Client secret\" (vous le trouverez à l'adresse https://developer.spotify.com/) : ")
        redirect_uri = input("Insérer votre \"Redirect URIs\" : ")
        from os import rename, path
        if path.exists("PrivateKey"):
            try :
                rename("PrivateKey", "PrivateKey.bak")
            except:
                print("Erreur lors de la création du fichier \"PrivateKey\".")
                return
        ecrire_fichier(".", "PrivateKey", f"{client_id}\n{client_secret}\n{redirect_uri}\n{logo}")


    from spotipy.oauth2 import SpotifyOAuth
    from spotipy import Spotify as Spotify_magic
    

    sp = Spotify_magic(auth_manager=SpotifyOAuth(client_id,client_secret,redirect_uri,scope="user-library-read"))
    liste_des_titres = []
    decalage = 0
    api_call = {'items' : []}
    if len(URL) != 22 or type(URL) != type(str(12)):
        print("Error invalid spotify url.")
        return None
    while len(api_call['items']) == 100 or decalage == 0:
        try:
            api_call = sp.playlist_tracks(URL, limit=100, offset=decalage)
            
        except:
            print("Error while searching spotify playlist.")
            return None
        for element in api_call['items']:
            liste_des_titres.append([element["track"]["name"],element["track"]["duration_ms"],element["track"]["artists"][0]["name"],element["track"]["album"]["images"][0]["url"]]) #["artists"][0,1,2,...]["name"] # Je ne prend que le premiere artiste.
        decalage += 100
    return liste_des_titres


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
    music_formats = {".mp3", ".m4a", ".wav", ".aac", ".ogg", ".pcm", ".caf", ".flac", ".alac", ".aiff", ".aif", ".dsd", ".dsf"}

    for _, _, fichiers in walk(dossier):  
        for fichier in fichiers:
            nom_fichier, extension = path.splitext(fichier)
            if extension.lower() in music_formats:
                fichiers_audio.append(nom_fichier)

    return fichiers_audio

# Exemple d'utilisation
chemin_de_depart = "."  # "." signifie le dossier actuel
liste_des_fichiers_audio = lister_fichiers_audio(chemin_de_depart)

a = tous_les_noms_d_une_playlist("2rBmkvV5eifqVNBfzcMDGZ")
print(a[0])