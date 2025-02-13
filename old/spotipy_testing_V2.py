import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="f24636adadff4a47ab4350e089ea7a71",client_secret="f318a45a20b74f47ac6d18a84e073b3e",redirect_uri="http://localhost:1234",scope="user-library-read"))

def tous_les_noms_d_une_playlist(URL):
    liste_des_titres = []
    decalage = 0
    api_call = {'items' : []}
    if len(URL) != 22:
        print("error invalid url")
        return None
    while len(api_call['items']) == 100 or decalage == 0:
        try:
            api_call = sp.playlist_tracks(URL, limit=100, offset=decalage)
            #print(api_call)
        except:
            print("error")
            return None
        for element in api_call['items']:
            liste_des_titres.append(element["track"]["name"])
        decalage += 100
    return liste_des_titres

JAAJ = str(input("URL"))
a = tous_les_noms_d_une_playlist(JAAJ)
print(len(a))