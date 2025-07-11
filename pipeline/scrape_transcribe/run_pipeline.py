"""
this script runs the base pipeline:
- scrapes youtube videos with a query and saves links
- downloads audio wav files from the scraped video links
- transcribes the audio files into json transcripts
"""


from pipeline.scrape_transcribe import scrape_youtube
from pipeline.scrape_transcribe import download_wav
from pipeline.scrape_transcribe import transcribe_json

def main():
    print("SCRAPE IN PROGRESS")
    scrape_youtube.scrape(query="behavioral interview answer", n_results=75) # change this, 2 was just for testing

    print("\nWAV DOWNLOAD IN PROGRESS")
    download_wav.download_wav(
        input_csv="data/scraped_links.csv",
        output_folder="data/downloaded_audio_new"
    )

    print("\nTRANSCRIPTION IN PROGRESS")
    transcribe_json.transcribe_json(
        input_folder="data/downloaded_audio_new",
        output_folder="data/asr_transcripts",
    )

if __name__ == "__main__":
    main()