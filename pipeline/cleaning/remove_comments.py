import json
from pathlib import Path

def strip_narrator_comments(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_data = []

    for entry in data:
        try:
            annotations = entry.get("annotations", [])
            if not annotations or not annotations[0].get("result"):
                continue

            original_answer = entry["data"]["answer"]
            result = annotations[0]["result"]

            spans = [
                (r["value"]["start"], r["value"]["end"])
                for r in result
                if r["type"] == "labels" and "Narrator Comment" in r["value"]["labels"]
            ]

            spans.sort(reverse=True)
            cleaned_answer = original_answer
            for start, end in spans:
                cleaned_answer = cleaned_answer[:start] + cleaned_answer[end:]

            entry["data"]["answer"] = cleaned_answer.strip()
            cleaned_data.append(entry)

        except Exception as e:
            print(f"Skipping item due to error: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print("Cleaned file saved:", output_file)

if __name__ == "__main__":
    input_path = r"data\labeled_dataset\project-2-at-2025-07-11-15-39-5826647e.json"
    output_path = r"data\labeled_dataset\project-2-cleaned.json"

    strip_narrator_comments(input_path, output_path)
