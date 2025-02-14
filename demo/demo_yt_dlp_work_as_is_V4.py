# merci chat.qwenlm.ai

import os
import yt_dlp

def download_soundcloud_music(url, output_folder="downloads"):
    """
    Télécharge une musique ou une liste de lecture depuis Soundcloud.

    Args:
        url (str): L'URL de la musique ou de la liste de lecture Soundcloud.
        output_folder (str): Dossier où sauvegarder les fichiers téléchargés.
    """
    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Options de configuration pour yt_dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Sélectionne la meilleure qualité audio disponible
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Convertit le fichier en mp3
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Qualité audio (en kbps)
        }],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Modèle pour le nom du fichier
        'restrictfilenames': True,  # Restreint les caractères spéciaux dans les noms de fichiers
        'noplaylist': False,  # Active le téléchargement des listes de lecture si l'URL en contient une
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Téléchargement en cours...")
            ydl.download([url])  # Télécharge l'URL donnée
        print(f"Téléchargement terminé. Les fichiers sont sauvegardés dans le dossier '{output_folder}'.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    # Demander à l'utilisateur l'URL Soundcloud
    soundcloud_url = input("Entrez l'URL de la musique ou de la liste de lecture Soundcloud : ")
    download_soundcloud_music(soundcloud_url)