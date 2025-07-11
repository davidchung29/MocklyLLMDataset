import json
from pathlib import Path
from collections import Counter
import statistics

def compute_stats(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    star_counts = Counter()
    quality_scores = []
    clarity_scores = []
    answer_lengths = []

    for item in data:
        try:
            result = item["annotations"][0]["result"]
            answer = item["data"]["answer"]
            clarity = item["data"].get("clarity", None)

            answer_lengths.append(len(answer.strip().split()))

            if isinstance(clarity, (int, float)):
                clarity_scores.append(clarity)

            for r in result:
                if r["type"] == "choices" and r["from_name"] == "quality_score":
                    choice = r["value"]["choices"][0]
                    quality_scores.append(int(choice))

                if r["type"] == "labels" and "labels" in r["value"]:
                    for label in r["value"]["labels"]:
                        star_counts[label] += 1
        except Exception as e:
            print(f"Error processing item: {e}")

    print("Dataset Statistics")
    print("-" * 40)

    print("\nLabel Frequencies:")
    for label, count in star_counts.items():
        print(f"{label}: {count}")

    if quality_scores:
        print("\nQuality Score (1–5):")
        print(f"Count: {len(quality_scores)}")
        print(f"Mean: {statistics.mean(quality_scores):.2f}")
        print(f"Median: {statistics.median(quality_scores):.2f}")

    if clarity_scores:
        print("\nClarity Score:")
        print(f"Count: {len(clarity_scores)}")
        print(f"Mean: {statistics.mean(clarity_scores):.4f}")
        print(f"Median: {statistics.median(clarity_scores):.4f}")

    if answer_lengths:
        print("\nAnswer Length (words):")
        print(f"Count: {len(answer_lengths)}")
        print(f"Mean: {statistics.mean(answer_lengths):.2f}")
        print(f"Median: {statistics.median(answer_lengths):.2f}")
        print(f"Max: {max(answer_lengths)}")
        print(f"Min: {min(answer_lengths)}")


if __name__ == "__main__":
    input_path = r"C:\Users\luzij\OneDrive\Documents\GitHub\MocklyLLMDataset\data\labeled_dataset\project-2-cleaned.json"
    compute_stats(input_path)
