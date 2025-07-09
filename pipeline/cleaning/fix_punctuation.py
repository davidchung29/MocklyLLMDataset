import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def is_question_api(text: str) -> bool:
    """Use API to determine if the sentence is a question."""
    prompt = f"Is the following sentence a question? Reply with 'yes' or 'no'.\n\n\"{text.strip()}\""
    data = {
        "model": "openai/gpt-4o",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"].strip().lower()
        return "yes" in reply
    else:
        print(f"API error: {response.status_code} - {response.text}")
        return False

def fix_punctuation(text: str) -> str:
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    if not text:
        return ""
    if text[-1] not in ".!?":
        if is_question_api(text):
            text += "?"
        else:
            text += "."

    return text[0].upper() + text[1:]

if __name__ == "__main__":
    examples = [
        "hello ",
        "   this is a test   ",
        "what time is it",
        "already punctuated!",
        " too many    spaces   here ",
        "can u help me",
        "it is sunny today",
        "where r u going",
        " "
    ]

    for s in examples:
        print(f"original: {repr(s)}")
        fixed = fix_punctuation(s)
        print(f"fixed:    {fixed}\n")