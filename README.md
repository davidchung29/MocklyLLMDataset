# MocklyLLMDataset

This project builds an end-to-end pipeline to collect, transcribe, clean, annotate, and analyze behavioral interview Q&A data. The output dataset enables evaluation of candidate interview responses with rich metadata.

## Project Structure

mocklyllmdataset/
├── data/
│   ├── asr_transcripts/
│   ├── downloaded_audio/
│   ├── qa_output/
│   ├── for_labeling/
│   ├── labeled_dataset/
│   └── scraped_links.csv
├── label_config/
│   └── star_config.xml
├── pipeline/
│   ├── scrape_transcribe/
│   │   ├── run_pipeline.py
│   │   ├── scrape_youtube.py
│   │   ├── download_wav.py
│   │   └── transcribe_json.py
│   ├── cleaning/
│   │   ├── basic/
│   │   │   ├── fix_punctuation.py
│   │   │   └── split_qa.py
│   │   ├── split_qa_synch.py
│   │   ├── split_qa_asynch.py
│   │   └── remove_comments.py
│   ├── prepare_labeling.py
│   └── data.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables in a `.env` file: