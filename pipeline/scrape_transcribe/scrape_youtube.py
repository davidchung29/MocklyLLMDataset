"""
this script searches youtube for videos matching a query
it saves the video urls (up to n_results) into a csv file

functions:
- scrape(query, n_results, output_csv): searches youtube and saves urls to csv
"""

import os
import csv
from yt_dlp import YoutubeDL

def scrape(
    query="behavioral interview answer",
    n_results=10,
    output_csv="data/scraped_links.csv"
):
    #os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    ydl_opts = {
        'quiet': True,
        'extract_flat': False,
        'skip_download': True,
        #'default_search': 'ytsearch',
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{n_results}:{query}", download=False)
    videos = info.get('entries', [])[:n_results]

    with open(output_csv, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["url"])
        for v in videos:
            if v and 'id' in v:
                writer.writerow([f"https://www.youtube.com/watch?v={v['id']}"])
    print(f"saved {len(videos)} videos to {output_csv}")

if __name__ == "__main__":
    scrape()
