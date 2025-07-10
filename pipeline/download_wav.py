"""
this script reads youtube urls from a csv file and downloads audio from each url
it saves the audio as webm files, then converts them to 16kHz mono wav files using ffmpeg
if the wav file already exists, it skips downloading and deletes the webm file
"""

import csv
import os
import subprocess
from yt_dlp import YoutubeDL

def download_wav(input_csv, output_folder):
    # ffmpeg_path = r'C:\ProgramData\chocolatey\bin\ffmpeg.exe' - this was b/c ffmpeg path was not added to myenv
    # os.makedirs(output_folder, exist_ok=True)

    # download audio only
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(id)s.%(ext)s'),
        'quiet': True,
        'noplaylist': True,  # REMINDER: change this when downloading playlist
    }

    with open(input_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['url']
            print(f'Downloading: {url}')
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                webm_file = os.path.join(output_folder, f"{info['id']}.webm")
                wav_file = os.path.join(output_folder, f"{info['id']}.wav")  # converted

                if os.path.exists(wav_file):
                    print(f"Already exists, skipping: {wav_file}")
                    if os.path.exists(webm_file):
                        os.remove(webm_file)
                    continue

                # command for webm --> wav
                command = [
                    "ffmpeg",
                    "-i", webm_file,
                    "-vn",
                    "-ar", "16000",  # adjust for quality/file size
                    "-ac", "1",
                    "-acodec", "pcm_s16le",
                    wav_file
                ]

                subprocess.run(command, check=True)
                print(f"Saved wav: {wav_file}")

                if os.path.exists(webm_file):
                    os.remove(webm_file)

if __name__ == "__main__":
    input_csv = 'data/scraped_links.csv'
    output_folder = 'data/downloaded_audio_new'
    download_wav(input_csv, output_folder)