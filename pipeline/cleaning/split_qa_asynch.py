"""
THIS IS THE ASYNCHRONOUS VERSION (faster)
processes transcribed JSON files to split text into q/a pairs using
an AI model API to classify sentences as questions. it uses asynchronous API calls for speed.

Functions:
- is_question_api(text: str) -> bool:
    async HTTP call to classify if a sentence is a question
- fix_punctuation(text: str) -> str:
    cleans punctuation and adds missing end punctuation base don sentence type
- split_into_qa(text) -> list:
    splits text into a list of dicts containing question-answer pairs.

*requires environment variable OPENROUTER_API_KEY for API authentication
"""

import os
import json
import re
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
semaphore = asyncio.Semaphore(12)
async_client = None


async def is_question_api(text: str) -> bool:
    async with semaphore:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a data cleaner. Your only job is to categorize whether a sentence is a question. "
                    "Do not alter or summarize the sentence. Only reply with 'yes' or 'no'."
                ),
            },
            {
                "role": "user",
                "content": f"""Here are some examples:

Sentence: "Can you describe a time when you had to lead a project under pressure and how you managed competing priorities, communicated with your team, and adjusted timelines to still meet the goal?"
Is it a question? Yes

Sentence: "During my internship at Amazon, I led a cross-functional project where I had to prioritize conflicting deadlines and manage communication between five teams."
Is it a question? No

Sentence: "Tell me about a failure you experienced and how you handled it."
Is it a question? Yes

Sentence: "I failed a major exam once but learned to manage my time better afterward."
Is it a question? No

Sentence: "{text.strip()}"
Is it a question?"""
            },
        ]
        data = {"model": "openai/gpt-4o", "messages": messages}
        try:
            response = await async_client.post(url, headers=headers, json=data, timeout=20)
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"].strip().lower()
            return "yes" in reply
        except Exception as e:
            print(f"API error on sentence: {text[:40]}... : {e}")
            return False


async def is_narrator_comment_api(text: str) -> bool:
    async with semaphore:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a text classifier. Determine if the sentence is a narrator or analyst comment "
                    "about the interview or interview questions. These are sentences that describe, analyze, or add context "
                    "but are NOT spoken by the interviewee or interviewer. Only reply with 'yes' or 'no'."
                ),
            },
            {
                "role": "user",
                "content": f"""Examples:

Sentence: "This question comes up all the time during Amazon area manager interviews."
Is it a narrator comment? Yes

Sentence: "I handled multiple priorities by staying organized and communicating well."
Is it a narrator comment? No

Sentence: "Many candidates struggle with this type of situational question."
Is it a narrator comment? Yes

Sentence: "I led a team that completed the project ahead of schedule."
Is it a narrator comment? No

Sentence: "{text.strip()}"
Is it a narrator comment?"""
            },
        ]
        data = {"model": "openai/gpt-4o", "messages": messages}
        try:
            response = await async_client.post(url, headers=headers, json=data, timeout=20)
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"].strip().lower()
            return "yes" in reply
        except Exception as e:
            print(f"API error on narrator comment check: {text[:40]}... : {e}")
            return False


async def fix_punctuation(text: str) -> str:
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    if not text:
        return ""
    if text[-1] not in ".!?":
        if await is_question_api(text):
            text += "?"
        else:
            text += "."
    return text[0].upper() + text[1:]


async def split_into_qa(text):
    text = await fix_punctuation(text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    qas = []
    question = None
    answer_parts = []
    i = 0
    while i < len(sentences):
        if await is_question_api(sentences[i]) and not await is_narrator_comment_api(sentences[i]):
            break
        i += 1
    while i < len(sentences):
        sent = sentences[i].strip()
        if await is_narrator_comment_api(sent):
            i += 1
            continue  # skip narrator/analyst comments
        if await is_question_api(sent):
            if question is not None and not answer_parts:
                question += " " + sent
            else:
                if question is not None:
                    raw_answer = " ".join(answer_parts).strip()
                    qas.append({"question": question, "answer": raw_answer})
                    answer_parts = []
                question = sent
        else:
            answer_parts.append(sent)
        i += 1
    if question is not None:
        answer = " ".join(answer_parts).strip()
        qas.append({"question": question, "answer": answer})
    return qas


async def process_file_async(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    full_text = data.get("text", "")
    return await split_into_qa(full_text)


async def main():
    global async_client
    async_client = httpx.AsyncClient()
    DATA_FOLDER = "data/asr_transcripts"
    OUTPUT_FOLDER = "data/qa_output"
    all_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]
    limit = input(f"{len(all_files)} JSON files. how many to process? (-1 for all): ")
    try:
        limit = int(limit)
    except ValueError:
        print("invalid input")
        limit = 0
    if limit == -1 or limit > len(all_files):
        limit = len(all_files)
    tasks = []
    for filename in all_files[:limit]:
        path = os.path.join(DATA_FOLDER, filename)
        print(f"processing {filename}")
        tasks.append(process_file_async(path))
    results = await asyncio.gather(*tasks)
    for filename, qa_pairs in zip(all_files[:limit], results):
        print(f"{len(qa_pairs)} Q&A pairs.")
        base_name = filename.replace(".wav.json", "")
        out_path = os.path.join(OUTPUT_FOLDER, base_name + "_qa.jsonl")
        with open(out_path, "w", encoding="utf-8") as out_file:
            for qa in qa_pairs:
                json_line = json.dumps(qa, ensure_ascii=False)
                out_file.write(json_line + "\n")
        print(f"saved to {out_path}\n")
    await async_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
