from fix_punctuation import fix_punctuation
from remove_filler import remove_filler

if __name__ == "__main__":
    examples = [
        "Uh, I was like going to the store, you know?",
        "So, um, actually I think it's okay.",
        "I mean, basically it's right there.",
        "Uh, um, okay, yes, I understand.",
        "No fillers here!",
        "Okay, let's start.",
        "Um... so, yeah, that's it.",
        "what time is it",
        "hello there",
        "can u help me"
    ]

    for text in examples:
        print(f"original: {repr(text)}")
        no_fillers = remove_filler(text)
        print(f"after remove_filler: {repr(no_fillers)}")
        fixed = fix_punctuation(no_fillers)
        print(f"after fix_punctuation: {repr(fixed)}\n")
