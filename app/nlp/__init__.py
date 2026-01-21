import nltk
import os

NLTK_DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "nltk_data"
)

os.makedirs(NLTK_DATA_DIR, exist_ok=True)

# Register custom NLTK data path
if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(NLTK_DATA_DIR)

# Only validate & download 'punkt'
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", download_dir=NLTK_DATA_DIR, quiet=True)
