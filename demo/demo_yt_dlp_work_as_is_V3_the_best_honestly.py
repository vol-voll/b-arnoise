import yt_dlp

# https://yt-dlp.memoryview.in/docs/embedding-yt-dlp/using-yt-dlp-in-python-scripts?_highlight=python

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        #'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])