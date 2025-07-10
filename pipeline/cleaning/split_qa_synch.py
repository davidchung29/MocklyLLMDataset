"""
processes transcribed JSON files to split text into q/a pairs using
an AI model API to classify sentences as questions. it uses synchronous API calls for speed.

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
import requests
from dotenv import load_dotenv
load_dotenv()
API_KEY=os.getenv("OPENROUTER_API_KEY")

url="https://openrouter.ai/api/v1/chat/completions"
headers={"Authorization": f"Bearer {API_KEY}",
         "Content-Type":"application/json"}

def is_question_api(text:str)->bool:
  messages=[
    {"role":"system",
     "content":(
       "You are a data cleaner. Your only job is to categorize whether a sentence is a question. "
       "Do not alter or summarize the sentence. Only reply with 'yes' or 'no'.")},
    {"role":"user",
     "content":f"""Here are some examples:

Sentence: "Can you describe a time when you had to lead a project under pressure and how you managed competing priorities, communicated with your team, and adjusted timelines to still meet the goal?"
Is it a question? Yes

Sentence: "During my internship at Amazon, I led a cross-functional project where I had to prioritize conflicting deadlines and manage communication between five teams."
Is it a question? No

Sentence: "Tell me about a failure you experienced and how you handled it."
Is it a question? Yes

Sentence: "I failed a major exam once but learned to manage my time better afterward."
Is it a question? No

Sentence: "{text.strip()}"
Is it a question?"""}
  ]
  data={
    "model":"openai/gpt-4o",
    "messages":messages
  }
  try:
    response=requests.post(url,headers=headers,json=data,timeout=20)
    response.raise_for_status()
    reply=response.json()["choices"][0]["message"]["content"].strip().lower()
    return "yes" in reply
  except Exception as e:
    print(f"API error on sentence: {text[:40]}... : {e}")
    return False

def fix_punctuation(text:str)->str:
  text=text.strip()
  text=re.sub(r'\s+',' ',text)
  if not text:
    return ""
  if text[-1] not in ".!?":
    if is_question_api(text):
      text+="?"
    else:
      text+="."
  return text[0].upper()+text[1:]

def split_into_qa(text):
  text=fix_punctuation(text)
  sentences=re.split(r'(?<=[.!?])\s+',text)

  qas=[]
  question=None
  answer_parts=[]

  i=0
  while i<len(sentences):
    if is_question_api(sentences[i]):
      break
    i+=1

  while i<len(sentences):
    sent=sentences[i].strip()
    if is_question_api(sent):
      if question is not None and not answer_parts:
        question+=" "+sent
      else:
        if question is not None:
          raw_answer=" ".join(answer_parts).strip()
          qas.append({"question":question,"answer":raw_answer})
          answer_parts=[]
        question=sent
    else:
      answer_parts.append(sent)
    i+=1

  if question is not None:
    answer=" ".join(answer_parts).strip()
    qas.append({"question":question,"answer":answer})

  return qas

def process_file(filepath):
  with open(filepath,"r",encoding="utf-8") as f:
    data=json.load(f)
  full_text=data.get("text","")
  return split_into_qa(full_text)

if __name__=="__main__":
  DATA_FOLDER="data/asr_transcripts"
  OUTPUT_FOLDER="data/qa_output"

  all_files=[f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]
  limit=input(f"{len(all_files)} JSON files. how many to process? (-1 for all): ")
  try:
    limit=int(limit)
  except ValueError:
    print("invalid input")
    limit=0

  if limit==-1 or limit>len(all_files):
    limit=len(all_files)

  for filename in all_files[:limit]:
    path=os.path.join(DATA_FOLDER,filename)
    print(f"processing {filename}")
    qa_pairs=process_file(path)
    print(f"{len(qa_pairs)} Q&A pairs.")

    base_name=filename.replace(".wav.json","")
    out_path=os.path.join(OUTPUT_FOLDER,base_name+"_qa.jsonl")
    with open(out_path,"w",encoding="utf-8") as out_file:
      for qa in qa_pairs:
        json_line=json.dumps(qa,ensure_ascii=False)
        out_file.write(json_line+"\n")
    print(f"saved to {out_path}\n")