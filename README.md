# MocklyLLMDataset
This project will build an end-to-end pipeline to source, transcribe, clean, and annotate behavioral-interview Q&amp;A data. The project will be used in the future to provide high-quality, well-labeled transcripts that will serve as the foundation for evaluating candidate responses.

Project Structure
mocklyllmdataset/
├── data/
│ ├── asr_transcripts/
│ ├── downloaded_audio/
│ ├── qa_output/
│ ├── for_labeling/
│ ├── labeled_dataset/
│ └── scraped_links.csv
├── label_config/
│ └── star_config.xml
├── pipeline/
│ ├── scrape_transcribe/
│ │ ├── run_pipeline.py
│ │ ├── scrape_youtube.py
│ │ ├── download_wav.py
│ │ └── transcribe_json.py
│ ├── cleaning/
│ │ ├── basic/
│ │ │ ├── fix_punctuation.py
│ │ │ └── split_qa.py
│ │ ├── split_qa_synch.py
│ │ ├── split_qa_asynch.py
│ │ └── remove_comments.py
│ ├── prepare_labeling.py
│ └── data.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
Setup
Create and activate a Python virtual environment.
Install dependencies: pip install -r requirements.txt
Set environment variables in a .env file:
OPENAI_API_KEY=your_api_key_here
LOCAL_FILES_SERVING_ENABLED=true
LOCAL_FILES_DOCUMENT_ROOT=path/to/your/for_labeling/folder
Usage
Run full pipeline: python pipeline/scrape_transcribe/run_pipeline.py
Clean and split transcripts into question-answer pairs:
Basic: python pipeline/cleaning/basic/split_qa.py
OpenAI API (sync): python pipeline/cleaning/split_qa_synch.py
OpenAI API (async): python pipeline/cleaning/split_qa_asynch.py
Convert split Q&A to Label Studio format: python pipeline/prepare_labeling.py
Start Label Studio locally: label-studio start
Post-processing:
Remove narrator comments: python pipeline/cleaning/remove_comments.py
Compute dataset statistics: python pipeline/data.py
Notes and Future Work
Implement improved narrator comment removal
Integrate cloud storage for wav files
Build mini dashboards to visualize dataset coverage