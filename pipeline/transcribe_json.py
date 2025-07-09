# uses OpenAI's Whisper ASR system to transcribe wav files
import os
import whisper
import json

def transcribe_json(input_folder, output_folder):
    # os.makedirs(output_folder, exist_ok=True)
    model = whisper.load_model("tiny")  # faster but less accurate

    for file in os.listdir(input_folder):
        if file.lower().endswith(".wav"):
            json_filename = file + ".json"
            output_path = os.path.join(output_folder, json_filename)

            if os.path.exists(output_path):
                print(f"already exists, skipping: {json_filename}")
                continue

            input_path = os.path.join(input_folder, file)
            print(f"Currently transcribing {file}")
            result = model.transcribe(input_path)

            simplified = [  # just id and text
                {"id": seg["id"], "text": seg["text"].strip()}
                for seg in result["segments"]
            ]
            output_data = {
                "file": file,
                "text": result["text"],
                "segments": simplified,
            }

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2)
            print(f"Successfully saved to {output_path}")
    
    print("DONE")


if __name__ == "__main__":
    input_folder = "data/downloaded_audio_new"
    output_folder = "data/asr_transcripts"
    transcribe_json(input_folder, output_folder)