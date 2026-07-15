#!/usr/bin/env python3

import argparse
import json
import time
from pathlib import Path

import requests


URLS = {
    "posts": "https://arctic-shift.photon-reddit.com/api/posts/search",
    "comments": "https://arctic-shift.photon-reddit.com/api/comments/search",
}

IDENTITY_FIELDS = {
    "author",
    "author_cakeday",
    "author_flair_background_color",
    "author_flair_css_class",
    "author_flair_richtext",
    "author_flair_template_id",
    "author_flair_text",
    "author_flair_text_color",
    "author_flair_type",
    "author_fullname",
    "author_patreon_flair",
    "author_premium",
    "author_id",
    "approved_by",
    "banned_by",
    "distinguished",
    "mod_reports",
    "user_reports",
}


def load_subreddits(path):
    seen = set()
    subreddits = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        subreddit = line.strip().removeprefix("r/")
        if subreddit and subreddit not in seen:
            seen.add(subreddit)
            subreddits.append(subreddit)
    return subreddits


def anonymize(item):
    return {key: value for key, value in item.items() if key not in IDENTITY_FIELDS}


def fetch_batch(session, subreddit, kind, after, retries):
    params = {
        "subreddit": subreddit,
        "limit": "auto",
        "sort": "asc",
        "meta-app": "replication-package",
    }
    if after is not None:
        params["after"] = after

    for attempt in range(retries + 1):
        try:
            response = session.get(URLS[kind], params=params, timeout=60)
            response.raise_for_status()
            data = response.json().get("data", [])
            next_after = None
            if data and "created_utc" in data[-1]:
                next_after = int(float(data[-1]["created_utc"]) * 1000) + 1
            return data, next_after
        except (requests.RequestException, json.JSONDecodeError):
            if attempt == retries:
                raise
            time.sleep(2**attempt)


def download(session, subreddit, kind, output_dir, start_ms, max_batches, sleep_seconds, overwrite, retries):
    subreddit_dir = Path(output_dir) / subreddit
    subreddit_dir.mkdir(parents=True, exist_ok=True)
    output_path = subreddit_dir / f"{subreddit}_{kind}.jsonl"

    if output_path.exists() and not overwrite:
        print(f"skip {output_path}")
        return

    after = start_ms
    batches = 0
    total = 0

    with output_path.open("w", encoding="utf-8") as output:
        while max_batches is None or batches < max_batches:
            data, next_after = fetch_batch(session, subreddit, kind, after, retries)
            if not data:
                break
            for item in data:
                output.write(json.dumps(anonymize(item), ensure_ascii=False) + "\n")
            batches += 1
            total += len(data)
            after = next_after
            if after is None:
                break
            time.sleep(sleep_seconds)

    print(f"{subreddit} {kind} {total}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subreddits", default="redditlist.txt")
    parser.add_argument("--output-dir", default="downloads/reddit")
    parser.add_argument("--posts", action="store_true")
    parser.add_argument("--comments", action="store_true")
    parser.add_argument("--start-ms", type=int)
    parser.add_argument("--max-batches", type=int)
    parser.add_argument("--sleep", type=float, default=1.0)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--retries", type=int, default=3)
    args = parser.parse_args()

    kinds = []
    if args.posts:
        kinds.append("posts")
    if args.comments:
        kinds.append("comments")
    if not kinds:
        kinds = ["posts", "comments"]

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 replication-package-downloader",
            "Accept": "application/json",
            "Referer": "https://arctic-shift.photon-reddit.com/",
        }
    )

    for subreddit in load_subreddits(args.subreddits):
        for kind in kinds:
            download(
                session,
                subreddit,
                kind,
                args.output_dir,
                args.start_ms,
                args.max_batches,
                args.sleep,
                args.overwrite,
                args.retries,
            )


if __name__ == "__main__":
    main()
