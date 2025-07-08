# THIS VERSION IS FOR PLAYLISTS, NOT SINGLE VIDEOS

import csv
import os
import subprocess
from yt_dlp import YoutubeDL

input_csv = 'data/playlist_links.csv'
output_folder = 'data/downloaded_audio_new'
os.makedirs(output_folder, exist_ok=True)

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(output_folder, '%(id)s.%(ext)s'),
    'quiet': True,
    'noplaylist': False, #now we can download playlist
}

with open(input_csv) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        playlist_url = row['url']
        print(f'current playlist: {playlist_url}')
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=True)
            entries = info_dict.get('entries', []) #entries is a list of video
            for video in entries:
                video_id = video['id']
                webm_file = os.path.join(output_folder, f"{video_id}.webm")
                wav_file = os.path.join(output_folder, f"{video_id}.wav")

                if os.path.exists(webm_file):  #if we alr made it a wav file before
                    command = [
                        "ffmpeg",
                        "-i", webm_file,
                        "-vn",
                        "-ar", "16000",
                        "-ac", "1",
                        "-acodec", "pcm_s16le",
                        wav_file
                    ]
                    subprocess.run(command, check=True)
                    print(f"Saved wav: {wav_file}")
                    os.remove(webm_file)
                else:
                    print(f"File not found: {webm_file}")