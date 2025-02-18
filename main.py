from weird_shenanigan import logo, the_true_b_and_a_magic
logo=logo()
the_true_b_and_a_magic()


def ecrire_fichier(folder_path, file_name, text):
    from os import path
    if type(text) == type([]):
        a = ""
        for i in text:
            a = a+str(i)+"\n"  
        text = a
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
        Key = lire_fichier("PrivateKey")
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
    music_formats = {".mp3", ".m4a", ".wav", ".aac", ".ogg", ".pcm", ".caf", ".flac", ".alac", ".aiff", ".aif", ".dsd", ".dsf", "ape", "mpga", "oga", "opus"}

    for _, _, fichiers in walk(dossier):  
        for fichier in fichiers:
            nom_fichier, extension = path.splitext(fichier)
            if extension.lower() in music_formats:
                fichiers_audio.append(nom_fichier)

    return fichiers_audio


def meme_nom(premier_nom,deuxieme_nom):
    """
    Vérifie si au moins un mot significatif du premier nom est présent dans le deuxième nom.

    Args:
        premier_nom (str): Le premier nom à comparer.
        deuxieme_nom (str): Le deuxième nom à comparer.

    Returns:
        bool: True si un mot du premier nom (d'au moins 4 lettres) est présent dans le deuxième nom, sinon False.
    """
    premier_nom, deuxieme_nom = premier_nom.lower(), deuxieme_nom.lower()

    if len(premier_nom) > len(deuxieme_nom):
        premier_nom, deuxieme_nom = deuxieme_nom, premier_nom
    liste_des_mot_du_premier_nom = premier_nom.split()

    liste_des_mot_du_premier_nom_final = liste_des_mot_du_premier_nom.copy()

    reglage_d_indice=0

    for indice in range(len(liste_des_mot_du_premier_nom)):
        if len(liste_des_mot_du_premier_nom[indice]) < 4:
            liste_des_mot_du_premier_nom_final.pop(indice-reglage_d_indice)
            reglage_d_indice+=1
    
    if liste_des_mot_du_premier_nom_final == []:
        liste_des_mot_du_premier_nom_final = liste_des_mot_du_premier_nom
    
    dictionnaire_des_mot_du_deuxieme_nom = dict(zip(deuxieme_nom.split(),[i for i in range(len(deuxieme_nom.split()))]))
    
    for mot in liste_des_mot_du_premier_nom_final:
        if mot in dictionnaire_des_mot_du_deuxieme_nom:
            return True
    return False


def chercher_youtube(recherche):
    from youtube_search import YoutubeSearch

    results = YoutubeSearch(str(recherche), max_results=1).to_dict()
    
    duration = results[0]["duration"].split(":")
    duration_ms = int(duration[0]) * 60000 + int(duration[1]) * 1000

    url = results[0]["url_suffix"]
    url = "http://youtube.com" + url

    return [results[0]["title"], duration_ms, results[0]["channel"], results[0]["thumbnails"][1], url]


def chercher_soundcloud(recherche):
    from playwright.sync_api import sync_playwright
    import re.search
    import urllib.parse.quote
 
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the target URL
        url = f"https://soundcloud.com/search?q={urllib.parse.quote(recherche)}"
        page.goto(url)

        # Wait for the search results to load
        page.wait_for_selector('div.searchItem')

        # Extract the first result
        results = page.query_selector_all('div.searchItem')
        if results:
            first_result = results[0]

            # Extract title and artist
            title = first_result.query_selector('a.soundTitle__title').inner_text()
            artist = first_result.query_selector('a.soundTitle__username').inner_text()
            link = first_result.query_selector('a.soundTitle__title').get_attribute('href')

            # Extract the image URL from the span's style attribute
            span_element = first_result.query_selector('span.sc-artwork')
            if span_element:
                style = span_element.get_attribute('style')
                # Use regex to extract the URL from the style attribute
                match = re.search(r'url\("([^"]+)"\)', style)
                if match:
                    image_url = match.group(1)
                else:
                    image_url = "Image URL not found."
            else:
                image_url = "No artwork span found."

            browser.close()
            return [title, "", artist, image_url, f"https://soundcloud.com{link}"]
            
        else:
            browser.close()


def download_music(url, output_folder=".", file_type="mp3"):
    """
    Télécharge une musique.

    Args:
        url (str): L'URL de la musique.
        output_folder (str): Dossier où sauvegarder les fichiers téléchargés.
    """
    from yt_dlp import YoutubeDL
    from os import path, makedirs

    if not path.exists(output_folder):
        makedirs(output_folder)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': file_type,
            #'preferredquality': '192',  # Qualité audio (en kbps)
        }],
        'outtmpl': path.join(output_folder, '%(title)s.%(ext)s'),
        'restrictfilenames': True,
        'noplaylist': False,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            print("Téléchargement en cours...")
            ydl.download([url])
    except Exception as e:
        print(f"Une erreur est survenue avec le téléchargement de {url}: {e}")


"""

print(meme_nom("SAINt JHN - Roses (Imanbek Remix)","SAINt JHN - Roses (Imanbek Remix) (Official Music Video)"))

print(chercher_youtube("SAINt JHN - Roses (Imanbek Remix)"))

download_music("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
"""

import os.path
if os.path.exists("option.txt"):
    try :
        url,chemin_d_enregistrement,platforme_d_enregistrement = lire_fichier("option.txt")[0], lire_fichier("option.txt")[1], lire_fichier("option.txt")[2]
    except:
        from os import rename
        from uuid import uuid4
        rename("option.txt", str(uuid4())+"option.txt")
    
if not os.path.exists("option.txt"):
    url = "empty"
    while len(url) != 22:
        url = input("Veuillez entrer la fin de l'URL de la playlist Spotify : ")
    
    chemin_d_enregistrement = "empty"
    while not os.path.exists(chemin_d_enregistrement):
        chemin_d_enregistrement = input("Veuillez indiquer l'emplacement d'enregistrement des fichiers musicaux ET où sont enregistrés vos anciens fichiers (. <=> ce fichier) : ")
    
    platforme_d_enregistrement=""
    while platforme_d_enregistrement.lower()!="youtube" and platforme_d_enregistrement.lower()!="soundcloud" and platforme_d_enregistrement.lower()!="s" and platforme_d_enregistrement.lower()!="y" and platforme_d_enregistrement.lower()!="sy" and platforme_d_enregistrement.lower()!="ys" and platforme_d_enregistrement != "":
        platforme_d_enregistrement = input("Préférez-vous télécharger sur YouTube, SoundCloud ou les deux ? Indiquez votre ordre de préférence. (s pour SoundCloud and y pour YouTube) (Default : sy) : ")
    platforme_d_enregistrement = platforme_d_enregistrement.lower()
    
    if platforme_d_enregistrement == "youtube":
        platforme_d_enregistrement = "y"
    elif platforme_d_enregistrement == "soundcloud":
        platforme_d_enregistrement = "s"
    elif platforme_d_enregistrement == "":
        platforme_d_enregistrement = "sy"
    
    a=""
    while a.lower()!="o" and a.lower()!="n" and a.lower()!="oui" and a.lower()!="non" and a!="":
        a = input("Voulez vous sauvgardez pour des prochaine utilisation ? (O ou n) : ") 
    
    if a.lower()!="o" or a.lower()!="oui" or a!="":
        ecrire_fichier(".","option.txt",[url,chemin_d_enregistrement])

liste_des_fichiers_audio = lister_fichiers_audio(chemin_d_enregistrement)
tous_les_songs_playlist = tous_les_noms_d_une_playlist(url)