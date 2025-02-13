import yt_dlp

ydl_opts = {}

def dwl_vid(video_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

channel = 1
while channel == 1:
    link_of_the_video = input("Copy & paste the URL of the YouTube video you want to download (PS : can downlowd playlist): ")
    zxt = link_of_the_video.strip()

    dwl_vid(zxt)
    channel = int(input("Enter 1 if you want to download more videos\nEnter 0 if you are done: "))