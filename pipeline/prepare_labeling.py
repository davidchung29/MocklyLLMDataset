import os
import json
import re

FILLERS = [
    "uh", "um", "like", "you know", "i mean",
    "so", "actually", "basically"
]

def get_clarity(text: str) -> float:
    """
    count filler words in the text and return filler_count / total_word_count
    does not remove any words from the text
    """
    text_lower = text.lower()
    total_words = len(re.findall(r"\b\w+\b", text_lower))
    if total_words == 0:
        return 0.0

    filler_count = 0

    for phrase in [f for f in FILLERS if " " in f]:
        pattern = r"\b" + re.escape(phrase) + r"\b"
        matches = re.findall(pattern, text_lower)
        filler_count += len(matches)

    words = re.findall(r"\b\w+\b", text_lower)
    filler_count += sum(1 for word in words if word in FILLERS)

    return round(filler_count / total_words, 4)

def combine_and_enrich(input_folder: str, combined_output_file: str):
    """
    combines all jsonl files in input_folder into one jsonl file with extra fields:
    - wraps inside { "id": ..., "data": { ... } }
    - empty STAR fields
    - null quality
    - clarity score
    """
    uid = 1
    os.makedirs(os.path.dirname(combined_output_file), exist_ok=True)

    with open(combined_output_file, "w", encoding="utf-8") as out_f:
        for filename in os.listdir(input_folder):
            if filename.endswith(".jsonl"):
                path = os.path.join(input_folder, filename)
                with open(path, "r", encoding="utf-8") as in_f:
                    for line in in_f:
                        try:
                            item = json.loads(line)
                            clarity = get_clarity(item.get("answer", ""))
                            enriched = {
                                "id": str(uid),
                                "data": {
                                    "question": item.get("question", ""),
                                    "answer": item.get("answer", ""),
                                    "situation": "",
                                    "task": "",
                                    "action": "",
                                    "result": "",
                                    "quality": None,
                                    "clarity": clarity
                                }
                            }
                            out_f.write(json.dumps(enriched, ensure_ascii=False) + "\n")
                            uid += 1
                        except Exception as err:
                            print(f"skipped one due to error: {err}")

    print(f"saved combined file to: {combined_output_file}")

def jsonl_to_json_array(jsonl_path: str, json_path: str):
    """
    reads a jsonl file and converts it to a json array file
    """
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    with open(jsonl_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    data = [json.loads(line) for line in lines]

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"saved json array file to: {json_path}")

def main():
    input_folder = "data/qa_output"
    combined_output_file = "data/for_labeling/star_data/combined_star_clarity.jsonl"
    json_array_output_file = "data/for_labeling/star_data/combined_star_clarity_array.json"

    combine_and_enrich(input_folder, combined_output_file)
    jsonl_to_json_array(combined_output_file, json_array_output_file)

if __name__ == "__main__":
    main()
