import os
import json
import re
from fix_punctuation import fix_punctuation
from remove_filler import remove_filler

DATA_FOLDER = "data/asr_transcripts"
OUTPUT_FOLDER = "data/qa_output"

QUESTION_WORDS = (
    "what", "where", "why", "how",
    "do", "did", "does", "can", "could", "would", "should",
    "are", "will",
    "tell me", "describe", "give me", "can you", "if you could",
    "explain", "walk me through", "how would you"
)

def is_question(sentence):
    sentence = sentence.strip().lower()
    if sentence.endswith('?'):
        return True
    for w in QUESTION_WORDS:
        if sentence.startswith(w):
            return True
    return False

def split_into_qa(text):
    text = remove_filler(text)
    text = fix_punctuation(text)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    qas = []
    question = None
    answer_parts = []

    i = 0
    while i < len(sentences) and not is_question(sentences[i]):
        i += 1

    while i < len(sentences):
        sent = sentences[i].strip()
        if is_question(sent):
            if question is not None and not answer_parts:
                question += " " + sent
            else:
                if question is not None:
                    answer = " ".join(answer_parts).strip()
                    qas.append({"question": question, "answer": answer})
                    answer_parts = []
                question = sent
        else:
            answer_parts.append(sent)
        i += 1

    # Append last Q&A
    if question is not None:
        answer = " ".join(answer_parts).strip()
        qas.append({"question": question, "answer": answer})

    return qas

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    full_text = data.get("text", "")
    return split_into_qa(full_text)

if __name__ == "__main__":
    # os.makedirs(OUTPUT_FOLDER, exist_ok=True)
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
