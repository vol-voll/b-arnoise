from weird_shenanigan import logo, the_true_b_and_a_magic
from youtube_search import YoutubeSearch
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify as Spotify_magic
import yt_dlp
from os import path, rename, remove
from mutagen.mp4 import MP4, MP4Cover
import urllib.request

logo=logo()
the_true_b_and_a_magic()
def ecrire_fichier(folder_path, file_name, text):
    if not path.exists(folder_path):
        print("The specified directory does not exist.")
    else:
        full_file_path = path.join(folder_path, file_name)

        if path.exists(full_file_path):
            file = open(full_file_path, 'a', encoding="utf-8")
        else:
            file = open(full_file_path, 'w', encoding="utf-8")

        file.write(text)
        file.close()

def lire_fichier(chemin_fichier,coupe = ""):
    """
    Lit un fichier texte et cree une liste pour chaque ligne.

    Args:
        chemin_fichier (str): Chemin du fichier à lire.
        coupe (str): Entre quelle caractaire couper "" <=> "\\n" 

    Returns:
        list: Liste contenant chaque ligne.
    """
    variables = []

    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()

    for i, ligne in enumerate(lignes):
        variables.append(ligne.strip())

    return variables

class Chanson:
    def __init__(soi, titre, artistes, album, dur, lienPoc, uri, NPlaylist, NomVideoYT="", LienVideoYT=""):
        soi.Titre = titre
        try : #Importé depuis spotify
            soi.ArtistePrincipal = artistes[0]['name']
            if len(artistes) > 1:
                soi.ArtistesSecondaires = []
                for Monsieur in artistes[1:]:
                    soi.ArtistesSecondaires.append(Monsieur['name'])
        except TypeError: #Importé depuis un .json
            soi.ArtistePrincipal = artistes
        soi.album = album
        soi.Duree = dur
        soi.Pochette = lienPoc
        soi.lien = uri
        soi.NomVideo = NomVideoYT
        soi.LienVideo = LienVideoYT
        soi.telechargee = soi.Titre+" - "+soi.ArtistePrincipal in fichiers_audio
        soi.NomPlaylist = NPlaylist

    def searchYt(soi):
        soi.liensValables = []
        try : 
            results = YoutubeSearch(soi.Titre+' - '+soi.ArtistePrincipal+' '+str(soi.ArtistesSecondaires), max_results=5).to_dict()
        except AttributeError:
            results = YoutubeSearch(soi.Titre+' - '+soi.ArtistePrincipal, max_results=5).to_dict()
        for chanson in results:
            chanson = (chanson['title'], chanson['duration'], chanson['url_suffix'][:20])
            delta=duration_comparison(soi.Duree, chanson)
            if delta!=None and name_comparison(soi, chanson):
                soi.liensValables.append([chanson[0], chanson[2], round(delta/1000,3)])
        if len(soi.liensValables) !=0 :        
            soi.liensValables.sort(key=ComparaisonDelta)
            soi.BestBanger = soi.liensValables[0]
            soi.NomVideo, soi.LienVideo= soi.BestBanger[0], soi.BestBanger[1]


    def changerYt(soi, lien):
        soi.LienVideo = lien

    def Telecharger(soi):
        ydl_opts = {'format': 'bestaudio/best','--ffmpeg-location' : "C:\\Users\\breva\\AppData\\Local\\Temp\\ffmpeg-7.1.1-full_build\\bin\\ffmpeg.exe",'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a',}],'outtmpl': path.join(f"downloads/{soi.NomPlaylist}", '%(title)s.%(ext)s'),'restrictfilenames': False,'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['http://youtube.com'+soi.LienVideo])
            urllib.request.urlretrieve(soi.Pochette, "Pochette.jpg")
            soi.telechargee = True
            try:
                audio = MP4("downloads/"+soi.NomPlaylist+"/"+soi.NomVideo+'.m4a')
                audio["\xa9nam"]=soi.Titre #Todo Intégrer les artistes secondaires quand ils sont là
                audio['\xa9alb'] = soi.album
                audio["\xa9ART"]=soi.ArtistePrincipal
                with open("Pochette.jpg", 'rb') as pochette:
                    audio['covr']=[MP4Cover(pochette.read(), imageformat=MP4Cover.FORMAT_JPEG)]
                audio.save()
            except Exception as e:
                print(f"Une erreur lors de l'édition de {soi.NomVideo}: {e}")
                #ecrire_fichier(".", "Reports", f"\nUne erreur lors de l'édition de {ProcessedBanger['nomChanson']} - {ProcessedBanger['ArtistePrincipal']}, cause : {e}")
            remove('Pochette.jpg')
            rename("downloads/"+soi.NomPlaylist+"/"+soi.NomVideo+'.m4a', "downloads/"+soi.NomPlaylist+"/"+soi.Titre+' - '+soi.ArtistePrincipal+".m4a")

def ComparaisonDelta(x):
    return x[2]

def name_comparison(rech : Chanson, prop):
    return (rech.ArtistePrincipal.lower() in prop[0].lower() or rech.Titre.lower() in prop[0].lower())
    #todo : Tenter un for any mais il faut gérer le bordel déjà

def duration_comparison(rech, prop):
    duration = prop[1].split(":")
    duration_ms = int(duration[0]) * 60000 + int(duration[1]) * 1000
    delta=abs(duration_ms-rech)
    if delta<5000 :
        return delta
    else :
        return None
    
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
    music_formats = {".mp3", ".m4a", ".wav", ".aac", ".ogg", ".pcm", ".caf", ".flac", ".alac", ".aiff", ".aif", ".dsd", ".dsf", "ape", "mpga", "oga", "opus"}

    for _, _, fichiers in walk(dossier):  
        for fichier in fichiers:
            nom_fichier, extension = path.splitext(fichier)
            if extension.lower() in music_formats:
                fichiers_audio.append(nom_fichier)

    return fichiers_audio


fichiers_audio = lister_fichiers_audio('downloads')