import requests
# don't look at this 3:28 AM AI code...
def search_soundcloud(query, client_id):
    url = f"https://api.soundcloud.com/tracks?client_id={client_id}&q={query}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erreur lors de la requête : {response.status_code}")
        return

    results = response.json()

    if not results:
        print("Aucun résultat trouvé.")
        return

    for idx, track in enumerate(results, start=1):
        print(f"{idx}. {track['title']} - Par {track['user']['username']} - Lien: {track['permalink_url']}")

if __name__ == "__main__":
    CLIENT_ID = ''
    recherche = input("Entrez votre recherche SoundCloud : ")
    search_soundcloud(recherche, CLIENT_ID)