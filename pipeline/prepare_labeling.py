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

def combine_and_enrich(input_folder: str, output_file: str):
    """
    combines all jsonl files in input_folder into one jsonl file with extra fields:
    - wraps inside { "id": ..., "data": { ... } }
    - empty STAR fields
    - null quality
    - clarity score
    """
    uid = 1
    with open(output_file, "w", encoding="utf-8") as out_f:
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
    print(f"saved file to: {output_file}")

def main():
    input_folder = "data/qa_output"
    output_file = "data/for_labeling/combined_star_clarity.jsonl"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    combine_and_enrich(input_folder, output_file)

if __name__ == "__main__":
    main()
