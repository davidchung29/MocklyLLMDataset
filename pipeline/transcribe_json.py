import os
import whisper
import json

input_folder = "data/downloaded_audio"
output_folder = "data/asr_transcripts"
#os.makedirs(output_folder, exist_ok=True)
model = whisper.load_model("base")  #faster but less accurate

for file in os.listdir(input_folder):
    if file.lower().endswith(".wav"):
        input_path = os.path.join(input_folder, file)
        print(f"currently transcribing {file}")
        result = model.transcribe(input_path)

        # simplified = [
        #     {k: seg[k] for k in ("id", "start", "end", "text")}
        #     for seg in result["segments"]
        # ]

        simplified = [ #just id and text
            {"id": seg["id"], "text": seg["text"].strip()}
            for seg in result["segments"]
        ]
        output_data = {
            "file": file,
            "text": result["text"],
            "segments": simplified,
        }

        output_path = os.path.join(output_folder, file + ".json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
        print(f"successfully saved to {output_path}")
print("DONE")
