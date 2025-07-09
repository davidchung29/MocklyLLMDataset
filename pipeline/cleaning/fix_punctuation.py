import re


def is_question(text):
    text = text.strip().lower()
    if text.endswith('?'):
        return True
    question_starters = (
        "who", "what", "when", "where", "why", "how",
        "do", "did", "does", "can", "could", "would", "should",
        "are", "will"
    )
    for starter in question_starters:
        pattern = rf"^{starter}\b"
        if re.match(pattern, text):
            return True
    return False

def fix_punctuation(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    if text and text[-1] not in '.!?':
        if is_question(text):
            text += '?'
        else:
            text += '.'
    return text[0].upper() + text[1:] if text else text

if __name__ == "__main__":
    example = [
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

    for s in example:
        print(f"original: {repr(s)}")
        print(f"fixed:    {fix_punctuation(s)}\n")