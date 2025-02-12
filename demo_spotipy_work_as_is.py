import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="f24636adadff4a47ab4350e089ea7a71",client_secret="f318a45a20b74f47ac6d18a84e073b3e",redirect_uri="http://localhost:1234",scope="user-library-read"))

uri = 'spotify:artist:1WgXqy2Dd70QQOU7Ay074N'

results = sp.artist_top_tracks(uri)#, limit=10)

print(results)

for track in results['tracks'][:10]:
    print('track    : ' + str(track['name']))
    print('audio    : ' + str(track['preview_url']))
    print('cover art: ' + str(track['album']['images'][0]['url']))
    print()