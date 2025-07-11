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