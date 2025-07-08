from pipeline import scrape_youtube
from pipeline import download_wav
from pipeline import transcribe_json

def main():
    print("SCRAPE IN PROGRESS")
    scrape_youtube.scrape(query="behavioral interview answer", n_results=1) # change this, 1 was just for testing

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