# MocklyLLMDataset
This project will build an end-to-end pipeline to source, transcribe, clean, and annotate behavioral-interview Q&amp;A data. The project will be used in the future to provide high-quality, well-labeled transcripts that will serve as the foundation for evaluating candidate responses.

# MocklyLLMDataset

this project builds an end-to-end pipeline to collect, transcribe, clean, annotate, and analyze behavioral interview q&a data. the output dataset will enable evaluation of candidate interview responses with rich metadata.

mocklyllmdataset/
│
├── data/
│ ├── asr_transcripts/ # transcribed json files from whisper (wav → text)
│ ├── downloaded_audio/ # wav files from video downloads
│ ├── qa_output/ # .jsonl files split into q&a pairs (post-cleaning + api)
│ ├── for_labeling/ # array of json-formatted q&a data for label studio
│ ├── labeled_dataset/ # exported and cleaned json files from label studio
│ └── scraped_links.csv # csv of scraped youtube links
│
├── label_config/
│ └── star_config.xml # star annotation config for label studio
│
├── pipeline/
│ ├── scrape_transcribe/ # raw data ingestion and transcription pipeline
│ │ ├── run_pipeline.py # master script for scrape + download + transcribe
│ │ ├── scrape_youtube.py # scrapes youtube links based on query
│ │ ├── download_wav.py # downloads individual youtube videos to .wav
│ │ └── transcribe_json.py # transcribes .wav files into json using whisper
│ │
│ ├── cleaning/
│ │ ├── basic/
│ │ │ ├── fix_punctuation.py # rule-based punctuation fixing + capitalization
│ │ │ └── split_qa.py # rule-based splitting of text into q&a pairs
│ │ │
│ │ ├── split_qa_synch.py # synchronous openai api-based q&a splitting
│ │ ├── split_qa_asynch.py # asynchronous version openai api (includes fix_punctuation)
│ │
│ ├── data.py # dataset statistics (label counts, clarity, lengths)
│ ├── prepare_labeling.py # formats q/a for annotation, jsonl → array of jsons
│ └── remove_comments.py # removes narrator comments using star-labeled data
│
├── .env # contains api keys and environment variables
├── .gitignore # ignores venv, .env, audio files, etc.
├── requirements.txt # all python packages used in the project
└── README.md # project description, setup, usage, and goals

setup
create and activate python virtual environment
install dependencies:

nginx
Copy
Edit
pip install -r requirements.txt
set environment variables (in a .env file):

ini
Copy
Edit
OPENAI_API_KEY=your_api_key_here
LOCAL_FILES_SERVING_ENABLED=true
LOCAL_FILES_DOCUMENT_ROOT=path/to/your/for_labeling/folder
note: if you don’t want to use openai api, you can use the rule-based version of q/a pair splitting in pipeline/cleaning/basic

usage
run full pipeline: scrape, download wav, transcribe

bash
Copy
Edit
python pipeline/scrape_transcribe/run_pipeline.py
clean and split transcripts into question-answer pairs

basic fix punctuation and split q&a:

bash
Copy
Edit
python pipeline/cleaning/basic/split_qa.py
or use OpenAI API (sync or async) for better splitting:

bash
Copy
Edit
python pipeline/cleaning/split_qa_synch.py
python pipeline/cleaning/split_qa_asynch.py
convert split q&a to label studio format:

bash
Copy
Edit
python pipeline/prepare_labeling.py
labeling

start label studio locally:

css
Copy
Edit
label-studio start
paste the xml file in settings/interface/code and paste the path to the json in local storage

post-processing

remove narrator comments from labeled data:

bash
Copy
Edit
python pipeline/cleaning/remove_comments.py
compute dataset statistics:

bash
Copy
Edit
python pipeline/data.py
notes and future work
implement improved narrator comment removal

integrate cloud storage for wav files

build mini dashboards to visualize dataset coverage