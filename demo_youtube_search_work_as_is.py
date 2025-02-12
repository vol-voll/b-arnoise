from youtube_search import YoutubeSearch

results = YoutubeSearch('Bang Bang dual', max_results=1).to_dict()

a = results[0]["url_suffix"]
a = "http://youtube.com" + a
print(a)