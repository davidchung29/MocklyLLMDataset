import re
import string

FILLERS = [
    "uh", "um", "like", "you know", "i mean",
    "so", "actually", "basically"
]
pattern = re.compile(
    r'\b(' + '|'.join(re.escape(filler) for filler in FILLERS) + r')\b',
    flags=re.IGNORECASE
)

def remove_filler(text):
    cleaned_text = pattern.sub('', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = cleaned_text.strip()
    #cleaned_text = re.sub(r'[{}]+$'.format(re.escape(string.punctuation)), '', cleaned_text)
    cleaned_text = re.sub(r'^[\s{}]+'.format(re.escape(string.punctuation)), '', cleaned_text)
    cleaned_text = re.sub(r'[\s{}]+$'.format(re.escape(string.punctuation)), '', cleaned_text)

    if cleaned_text:
        cleaned_text = cleaned_text[0].upper() + cleaned_text[1:]
    return cleaned_text

if __name__ == "__main__":
    examples = [
        "Uh, I was like going to the store, you know?",
        "So, um, actually I think it's okay.",
        "I mean, basically it's right there.",
        "Uh, um, okay, yes, I understand.",
        "No fillers here!",
        "Okay, let's start.",
        "Um... so, yeah, that's it."
    ]
    for s in examples:
        print(f"original: {repr(s)}")
        print(f"filtered:  {remove_filler(s)}\n")
