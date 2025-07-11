# MocklyLLMDataset

This project builds an end-to-end pipeline to source, transcribe, clean, and annotate
behavioral-interview Q&A data. The project will be used in the future to provide high-quality,
well-labeled transcripts that will serve as the foundation for evaluating candidate responses.

## Project Structure

mocklyllmdataset/
│
├── data/
│   ├── asr_transcripts/           # transcribed json files from whisper (wav → text)
 
│   ├── downloaded_audio/          # wav files from video downloads
 
│   ├── qa_output/                 # .jsonl files split into q&a pairs (post-cleaning + api)
 
│   ├── for_labeling/              # array of json-formatted q&a data for label studio
 
│   ├── labeled_dataset/           # exported and cleaned json files from label studio
 
│   └── scraped_links.csv          # csv of scraped youtube links

│
├── label_config/
│   └── star_config.xml            # star annotation config for label studio

│
├── pipeline/
│   ├── scrape_transcribe/         # raw data ingestion and transcription pipeline
 
│   │   ├── run_pipeline.py        # master script for scrape + download + transcribe
 
│   │   ├── scrape_youtube.py      # scrapes youtube links based on query
 
│   │   ├── download_wav.py        # downloads individual youtube videos to .wav
 
│   │   └── transcribe_json.py     # transcribes .wav files into json using whisper

│   │
│   ├── cleaning/
│   │   ├── basic/
 
│   │   │   ├── fix_punctuation.py     # rule-based punctuation fixing + capitalization
 
│   │   │   └── split_qa.py            # rule-based splitting of text into q&a pairs

│   │   │
│   │   ├── split_qa_synch.py          # synchronous openai API-based q&a splitting
 
│   │   ├── split_qa_asynch.py         # asynchronous version openai api (includes fix_punctuation)

│   ├── data.py                        # dataset statistics (label counts, clarity, lengths)
 
│   ├── prepare_labeling.py            # formats q/a for annotation, jsonl → array of jsons
 
│   └── remove_comments.py             # removes narrator comments using star-labeled data

│
├── .env                               # contains api keys and environment variables
 
├── .gitignore                         # ignores venv, .env, audio files, etc.
 
├── requirements.txt                   # all python packages used in the project
 
└── README.md                          # project description, setup, usage, and goals

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables in a `.env` file:<br>
OPENAI_API_KEY=your_api_key_here<br>
LOCAL_FILES_SERVING_ENABLED=true<br>
LOCAL_FILES_DOCUMENT_ROOT=path/to/your/for_labeling/folder

## Usage

1. Run full pipeline: `python pipeline/scrape_transcribe/run_pipeline.py`
2. Clean and split transcripts into question-answer pairs:
- Basic: `python pipeline/cleaning/basic/split_qa.py`
- OpenAI API (sync): `python pipeline/cleaning/split_qa_synch.py`
- OpenAI API (async): `python pipeline/cleaning/split_qa_asynch.py`
3. Convert split Q&A to Label Studio format: `python pipeline/prepare_labeling.py`
4. Start Label Studio locally: `label-studio start`
5. Post-processing:
- Remove narrator comments: `python pipeline/cleaning/remove_comments.py`
- Compute dataset statistics: `python pipeline/data.py`

## Notes and Future Work
* Implement improved narrator comment removal
* Integrate cloud storage for wav files
* Build mini dashboards to visualize dataset coverage