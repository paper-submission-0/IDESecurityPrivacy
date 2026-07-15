#!/usr/bin/env python3

import argparse
import csv
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from threading import Lock


class PrivacyFilter:
    def __init__(self, model, ports, temperature):
        try:
            import ollama
        except ImportError as exc:
            raise RuntimeError("Install the 'ollama' Python package.") from exc

        if not model:
            raise ValueError("--model is required")
        if not ports:
            raise ValueError("--ports is required")

        self.model = model
        self.options = {"temperature": temperature} if temperature is not None else {}
        self.clients = [ollama.Client(host=f"http://localhost:{port}") for port in ports]
        self.index = 0
        self.lock = Lock()

    def next_client(self):
        with self.lock:
            client = self.clients[self.index]
            self.index = (self.index + 1) % len(self.clients)
            return client

    @staticmethod
    def parse_json(raw):
        raw = re.sub(r"<think>.*?</think>", "", raw or "", flags=re.DOTALL)
        raw = re.sub(r"```json|```", "", raw).strip()
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return {"decision": "no", "rationale": "model failed to produce valid JSON"}
        return {
            "decision": str(parsed.get("decision", "no")).strip().lower(),
            "rationale": str(parsed.get("rationale", "")),
        }

    def classify(self, text):
        if not text.strip():
            return {"decision": "no", "rationale": "empty text"}
        if text.strip().lower() in {"[removed]", "[deleted]"}:
            return {"decision": "no", "rationale": "removed or deleted body"}

        prompt = f"""
You are performing a binary classification task.
Analyze whether the Reddit post clearly describes a privacy risk, concern, violation, or threat involving an LLM-enabled IDE or coding assistant.

Answer yes only for privacy issues involving unauthorized collection, transmission, inference, retention, or disclosure of source code, personal data, proprietary information, or secrets caused by AI integration in development environments.
Answer no for all other cases.

Return only valid JSON:
{{"decision": "yes" or "no", "rationale": "a short one-sentence explanation"}}

Post:
```{text}```
"""
        response = self.next_client().generate(
            model=self.model,
            prompt=prompt,
            think=False,
            options=self.options,
        )
        return self.parse_json(response.get("response", ""))


def parse_ports(value):
    return [int(port.strip()) for port in value.split(",") if port.strip()]


def post_date(created_utc):
    try:
        return datetime.fromtimestamp(float(created_utc), tz=timezone.utc).strftime("%Y-%m-%d")
    except (TypeError, ValueError, OSError):
        return ""


def iter_jsonl_files(root_dir, suffix, subreddits):
    allowed = set(subreddits) if subreddits else None
    for dirpath, _, filenames in os.walk(root_dir):
        subreddit = os.path.basename(dirpath)
        if allowed is not None and subreddit not in allowed:
            continue
        for filename in filenames:
            if filename.endswith(suffix):
                yield os.path.join(dirpath, filename)


def load_posts(root_dir, suffix, subreddits):
    for path in iter_jsonl_files(root_dir, suffix, subreddits):
        with open(path, encoding="utf-8") as input_file:
            for line in input_file:
                line = line.strip()
                if not line:
                    continue
                try:
                    post = json.loads(line)
                except json.JSONDecodeError:
                    continue
                yield path, post


def process_post(item, classifier):
    filename, post = item
    title = post.get("title", "")
    selftext = post.get("selftext", "")
    if not isinstance(title, str):
        title = ""
    if not isinstance(selftext, str):
        selftext = ""
    result = classifier.classify(f"{title}\n{selftext}".strip())
    return {
        "filename": filename,
        "post_id": post.get("id", ""),
        "post_url": post.get("url", ""),
        "post_date": post_date(post.get("created_utc")),
        "LLMResp": result.get("decision", "no"),
        "rationale": result.get("rationale", ""),
        "title": title,
        "selftext": selftext,
    }


def load_subreddits(path):
    if not path:
        return []
    with open(path, encoding="utf-8") as input_file:
        return [line.strip().removeprefix("r/") for line in input_file if line.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-dir", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--ports", required=True)
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--jsonl-suffix", default="_posts.jsonl")
    parser.add_argument("--subreddits")
    parser.add_argument("--workers", type=int)
    args = parser.parse_args()

    ports = parse_ports(args.ports)
    workers = args.workers or len(ports)
    classifier = PrivacyFilter(args.model, ports, args.temperature)
    posts = list(load_posts(args.root_dir, args.jsonl_suffix, load_subreddits(args.subreddits)))

    fieldnames = ["filename", "post_id", "post_url", "post_date", "LLMResp", "rationale", "title", "selftext"]
    with open(args.output_csv, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(process_post, post, classifier) for post in posts]
            for completed, future in enumerate(as_completed(futures), start=1):
                writer.writerow(future.result())
                output_file.flush()
                if completed % 100 == 0:
                    print(f"Processed {completed}/{len(posts)}")


if __name__ == "__main__":
    main()
