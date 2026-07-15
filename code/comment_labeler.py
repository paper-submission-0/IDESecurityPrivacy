#!/usr/bin/env python3

import argparse
import csv
import json
import time

import requests


CONTROLLED_TOPICS = {
    "Secure IDE Configuration": "Secure configuration, permission management, access controls, secure defaults, auditing, vulnerability scanning, and general security or privacy recommendations.",
    "Sensitive File Protection": "Preventing AI tools from accessing, modifying, or leaking credentials, environment files, configuration files, private keys, or other sensitive files.",
    "Manual Code Verification": "Human review and validation of AI-generated code to detect errors, vulnerabilities, spam, or unsafe behavior.",
    "Use Version Control": "Using version control to track changes, support rollback, recovery, and accountability for AI-assisted code.",
    "Sandboxing": "Isolating AI agents, tools, or execution environments in restricted sandboxes.",
    "Memory/Context Isolation": "Preventing unintended persistence, reuse, or cross-session sharing of model memory, context, or data.",
    "Refer to Documentation": "Consulting official documentation for tool behavior, configuration, security implications, or limitations.",
    "Consult Vendors": "Seeking clarification, updates, or security assurances from AI IDE vendors or service providers.",
    "Disable Telemetry": "Disabling data collection, usage tracking, or telemetry to reduce privacy risks.",
    "Check Organizational Compliance": "Checking compliance with organizational policies, internal guidelines, legal requirements, or industry regulations.",
    "Logging and Monitoring": "Using logging and monitoring to observe AI actions, detect anomalies, and support auditing or incident investigation.",
    "Use Local LLM": "Using local or self-managed models instead of cloud-based services for stronger data and privacy control.",
    "Tool/Extension Monitoring": "Verifying, evaluating, and monitoring AI tools or IDE extensions before use.",
}

CONTROLLED_SET = set(CONTROLLED_TOPICS)


def build_prompt(comment_text):
    topics = "\n".join(f"- {topic}" for topic in CONTROLLED_TOPICS)
    return f"""
You are classifying actionable security, safety, or operational suggestions made by developers about AI coding assistants.

COMMENT:
\"\"\"{comment_text}\"\"\"

Select all applicable topics from the controlled list. Use exact labels only.
If none apply, return an empty matched_topics list.

CONTROLLED TOPICS:
{topics}

Output JSON only:
{{"matched_topics": ["topic1", "topic2"]}}
"""


def call_ollama(prompt, url, model, timeout, temperature):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {},
    }
    if temperature is not None:
        payload["options"]["temperature"] = temperature
    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json().get("response", "")


def parse_topics(raw):
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        return []
    matched = result.get("matched_topics", [])
    return sorted(topic for topic in matched if isinstance(topic, str) and topic in CONTROLLED_SET)


def label_comment(comment_text, url, model, timeout, temperature):
    try:
        raw = call_ollama(build_prompt(comment_text), url, model, timeout, temperature)
        return parse_topics(raw)
    except requests.RequestException:
        return []


def first_existing(row, names):
    for name in names:
        if name in row:
            return row.get(name, "")
    return ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--ollama-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--sleep", type=float, default=0)
    args = parser.parse_args()

    with open(args.input_csv, newline="", encoding="utf-8") as input_file, open(
        args.output_csv, "w", newline="", encoding="utf-8"
    ) as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(
            output_file,
            fieldnames=["post_id", "comment_id", "comment_index", "matched_topics"],
        )
        writer.writeheader()

        for index, row in enumerate(reader, start=1):
            comment_text = first_existing(row, ["comment_text", "Comment_text", "body", "text"])
            matched = label_comment(
                comment_text,
                args.ollama_url,
                args.model,
                args.timeout,
                args.temperature,
            )
            writer.writerow(
                {
                    "post_id": row.get("post_id", ""),
                    "comment_id": row.get("comment_id", ""),
                    "comment_index": row.get("comment_index", ""),
                    "matched_topics": ";".join(matched),
                }
            )
            output_file.flush()
            if args.sleep:
                time.sleep(args.sleep)
            if index % 5 == 0:
                print(f"Processed {index} comments")


if __name__ == "__main__":
    main()
