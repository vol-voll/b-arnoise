import yt_dlp

def download_audio(link):
  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    print(video_title)
    video.download(link)    
    print("Successfully Downloaded - see local folder on Google Colab")

download_audio('https://www.youtube.com/watch?v=cJuO985zF8E')