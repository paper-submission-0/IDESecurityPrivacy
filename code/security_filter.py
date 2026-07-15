#!/usr/bin/env python3

import argparse
import csv
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock


class SecurityFilter:
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
    def parse_answer(raw):
        raw = re.sub(r"<think>.*?</think>", "", raw or "", flags=re.DOTALL)
        match = re.search(r"\b(yes|no)\b", raw.strip().lower())
        return match.group(1) if match else "no"

    def classify(self, text):
        prompt = f"""
You are a security analyst reviewing Reddit posts.
Determine whether the post discusses a security vulnerability involving an LLM-enabled IDE or coding assistant.

Classify as Yes only if it involves data leaks, credential exposure, prompt injection, poisoned AI context, insecure generated code, or vulnerable IDE extensions/plugins caused by LLM integration.
Classify as No otherwise.

Respond only with Yes or No.

Reddit Post:
```{text}```
"""
        response = self.next_client().generate(
            model=self.model,
            prompt=prompt,
            think=False,
            options=self.options,
        )
        return self.parse_answer(response.get("response", ""))


def post_id_from_url(url):
    match = re.search(r"/comments/([^/]+)/", url or "")
    return match.group(1) if match else ""


def row_text(row):
    return "\n".join(
        value
        for value in [row.get("title", ""), row.get("selftext", ""), row.get("text", "")]
        if value
    )


def process_row(row, classifier):
    post_url = row.get("post_url", "") or row.get("url", "")
    post_id = row.get("post_id", "") or post_id_from_url(post_url)
    return {
        "post_url": post_url,
        "response": classifier.classify(row_text(row)),
        "post_id": post_id,
    }


def parse_ports(value):
    return [int(port.strip()) for port in value.split(",") if port.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--ports", required=True)
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--workers", type=int)
    parser.add_argument("--sleep", type=float, default=0)
    args = parser.parse_args()

    ports = parse_ports(args.ports)
    workers = args.workers or len(ports)
    classifier = SecurityFilter(args.model, ports, args.temperature)

    with open(args.input_csv, newline="", encoding="utf-8") as input_file:
        rows = list(csv.DictReader(input_file))

    with open(args.output_csv, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=["post_url", "response", "post_id"])
        writer.writeheader()

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(process_row, row, classifier) for row in rows]
            for completed, future in enumerate(as_completed(futures), start=1):
                writer.writerow(future.result())
                output_file.flush()
                if args.sleep:
                    time.sleep(args.sleep)
                if completed % 10 == 0:
                    print(f"Processed {completed}/{len(rows)}")


if __name__ == "__main__":
    main()
