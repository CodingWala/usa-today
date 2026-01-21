from app.pipeline import run_pipeline
import os

def main():
    source = os.getenv("NEWS_SOURCE", "yahoo")
    count = run_pipeline(source)
    print(f"Stored {count} articles")

if __name__ == "__main__":
    main()
