from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify as Spotify_magic

sp = Spotify_magic(auth_manager=SpotifyOAuth(client_id="f24636adadff4a47ab4350e089ea7a71",client_secret="f318a45a20b74f47ac6d18a84e073b3e",redirect_uri="http://localhost:1234",scope="user-library-read"))

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