import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="f24636adadff4a47ab4350e089ea7a71",client_secret="f318a45a20b74f47ac6d18a84e073b3e",redirect_uri="http://localhost:1234",scope="user-library-read"))


try:
    JAAJ = str(input("URL"))
    if len(JAAJ) != len("2rBmkvV5eifqVNBfzcMDGZ"):
        JAAJ = "2rBmkvV5eifqVNBfzcMDGZ"
    results = sp.playlist_tracks(JAAJ, limit=100, offset=1000)
    #print(results)
except:
    print("LOL ! Tu a écrit de la merde :3")


for element in results['items']:
    print(element["track"]["name"])
