import os
import json
import re
from fix_punctuation import fix_punctuation
from dotenv import load_dotenv
import requests

# Load environment variables for API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Define OpenRouter API endpoint and headers
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

DATA_FOLDER = "data/asr_transcripts"
OUTPUT_FOLDER = "data/qa_output"

# Use the API to decide if a sentence is a question
def is_question_api(sentence):
    prompt = f"Is the following sentence a question? Respond with yes or no.\n\n\"{sentence.strip()}\""
    data = {
        "model": "openai/gpt-4o",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"].strip().lower()
            return "yes" in reply
        else:
            print(f"API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"API request failed: {e}")
        return False

def split_into_qa(text):
    text = fix_punctuation(text)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    qas = []
    question = None
    answer_parts = []

    i = 0
    # Skip intro without question
    while i < len(sentences):
        if is_question_api(sentences[i]):
            break
        i += 1

    while i < len(sentences):
        sent = sentences[i].strip()
        if is_question_api(sent):
            if question and not answer_parts:
                question += " " + sent  # combine consecutive questions
            else:
                if question:
                    answer = " ".join(answer_parts).strip()
                    qas.append({"question": question, "answer": answer})
                    answer_parts = []
                question = sent
        else:
            answer_parts.append(sent)
        i += 1

    if question:
        answer = " ".join(answer_parts).strip()
        qas.append({"question": question, "answer": answer})

    return qas

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    full_text = data.get("text", "")
    return split_into_qa(full_text)

if __name__ == "__main__":
    all_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]
    limit = input(f"{len(all_files)} JSON files. how many to process? (-1 for all): ")
    try:
        limit = int(limit)
    except ValueError:
        print("invalid input")
        limit = 0

    if limit == -1 or limit > len(all_files):
        limit = len(all_files)

    for filename in all_files[:limit]:
        path = os.path.join(DATA_FOLDER, filename)
        print(f"processing {filename}")
        qa_pairs = process_file(path)
        print(f"{len(qa_pairs)} Q&A pairs.")

        base_name = filename.replace(".wav.json", "")
        out_path = os.path.join(OUTPUT_FOLDER, base_name + "_qa.jsonl")
        with open(out_path, "w", encoding="utf-8") as out_file:
            for qa in qa_pairs:
                json_line = json.dumps(qa, ensure_ascii=False)
                out_file.write(json_line + "\n")
        print(f"saved to {out_path}\n")
