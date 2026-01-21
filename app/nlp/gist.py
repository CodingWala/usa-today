import nltk
from nltk.tokenize import sent_tokenize

# ✅ Hard fix (no runtime crash)
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def generate_gist(text: str) -> str:
    if not text:
        return ""

    sentences = sent_tokenize(text)
    return sentences[0] if sentences else ""

import re

TRUMP_KEYWORDS = [
    "donald trump",
    "president trump",
    "former president trump",
    "trump campaign",
    "trump administration"
]

def clean_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_best_gist(article_text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", article_text)

    scored = []

    for idx, sentence in enumerate(sentences):
        s = sentence.lower()
        score = 0

        # Trump relevance
        score += sum(2 for k in TRUMP_KEYWORDS if k in s)

        # Early sentences are usually summary
        if idx < 3:
            score += 2

        # Penalize very short / long sentences
        if 20 < len(sentence) < 200:
            score += 1

        scored.append((score, sentence))

    scored.sort(reverse=True, key=lambda x: x[0])

    best = scored[0][1] if scored else ""
    return clean_sentence(best)
