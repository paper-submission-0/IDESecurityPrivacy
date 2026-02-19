import os
import json
import csv
import ollama

ROOT_DIR = "../reddit"
OUTPUT_CSV = "security_discussions.csv"
MODEL = "gpt-oss:120b"

PROMPT = ""

def classify(text):
    if not text:
        return ""
    r = ollama.generate(model=MODEL, prompt=PROMPT + text)
    return r.get("response", "").strip().lower()

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow(["file", "url", "label", "text"])

    for root, _, files in os.walk(ROOT_DIR):
        for name in files:
            if not name.endswith(".jsonl"):
                continue

            with open(os.path.join(root, name), encoding="utf-8") as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    text = obj.get("selftext", "")
                    label = classify(text)
                    writer.writerow([
                        name,
                        obj.get("url", ""),
                        label,
                        text
                    ])
