from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify as Spotify_magic
import os

LOGO = """
▄▄▄█████▓  ██░ ██  ▓█████      ▄▄▄▄        ▄▄▄      ██▀███   ███▄    █  ▒█████    ██▓  ██████  ▓█████
▓  ██▒ ▓▒▒▓██░ ██  ▓█   ▀     ▓█████▄     ▒████▄   ▓██ ▒ ██▒ ██ ▀█   █ ▒██▒  ██▒▒▓██▒▒██    ▒  ▓█   ▀
▒ ▓██░ ▒░░▒██▀▀██  ▒███       ▒██▒ ▄██    ▒██  ▀█▄ ▓██ ░▄█ ▒▓██  ▀█ ██▒▒██░  ██▒▒▒██▒░ ▓██▄    ▒███  
░ ▓██▓ ░  ░▓█ ░██  ▒▓█  ▄     ▒██░█▀   ██ ░██▄▄▄▄██▒██▀▀█▄  ▓██▒  ▐▌██▒▒██   ██░░░██░  ▒   ██▒ ▒▓█  ▄
  ▒██▒ ░  ░▓█▒░██▓▒░▒████    ▒░▓█  ▀█▓     ▓█   ▓██░██▓ ▒██▒▒██░   ▓██░░ ████▓▒░░░██░▒██████▒▒▒░▒████
  ▒ ░░     ▒ ░░▒░▒░░░ ▒░     ░░▒▓███▀▒     ▒▒   ▓▒█░ ▒▓ ░▒▓░░ ▒░   ▒ ▒ ░ ▒░▒░▒░  ░▓  ▒ ▒▓▒ ▒ ░░░░ ▒░ 
    ░      ▒ ░▒░ ░░ ░ ░      ░▒░▒   ░       ░   ▒▒   ░▒ ░ ▒ ░ ░░   ░ ▒░  ░ ▒ ▒░ ░ ▒ ░░ ░▒  ░ ░░ ░ ░  
  ░ ░      ░  ░░ ░    ░        ░    ░       ░   ▒    ░░   ░    ░   ░ ░ ░ ░ ░ ▒  ░ ▒ ░░  ░  ░      ░  
           ░  ░  ░░   ░      ░ ░                ░     ░              ░     ░ ░    ░        ░  ░   ░  
"""
print(LOGO)
sp = Spotify_magic(auth_manager=SpotifyOAuth(client_id="f24636adadff4a47ab4350e089ea7a71",client_secret="f318a45a20b74f47ac6d18a84e073b3e",redirect_uri="http://localhost:1234",scope="user-library-read"))


def create_a_file(folder_path,file_name,file_contents):
    full_file_path = os.path.join(folder_path, file_name)
    try:
        if os.path.exists(full_file_path):
            file = open(full_file_path, 'a')
        else:
            file = open(full_file_path, 'w')
    except:
            print("Error while creating file.")
            return None

    file.write(str(file_contents))

    file.close()


def all_spotify_playlist_song(URL):
    """
    Retrieves the list of tracks from a Spotify playlist given its URL.

    Args:
        URL (str): The unique identifier of the Spotify playlist.

    Returns:
        list: A list of tracks, where each track is represented as a list containing:
            - Track name (str)
            - Track duration in milliseconds (int)
            - Primary artist's name (str)
            - URL of the album cover image (str)
        
        Returns None if the URL is invalid or if an error occurs while fetching the playlist.

    Errors:
        - Prints an error message and returns None if the URL format is incorrect.
        - Prints an error message and returns None if an issue occurs while fetching the playlist from the Spotify API.
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
            create_a_file("","cache.temp",([element["track"]["name"],element["track"]["duration_ms"],element["track"]["artists"][0]["name"],element["track"]["album"]["images"][0]["url"]]))
            create_a_file("","cache.temp","\n")
        decalage += 100
    return liste_des_titres


a = all_spotify_playlist_song("2rBmkvV5eifqVNBfzcMDGZ")
print(a[0])
