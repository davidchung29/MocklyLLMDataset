import json

input_path = 'data/for_labeling/star_data/combined_star_clarity.jsonl'
output_path = 'data/for_labeling/star_data/combined_star_clarity_array.json'

with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

data = [json.loads(line) for line in lines]

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
