import requests
import json
import time

POSTS_URL = "https://arctic-shift.photon-reddit.com/api/posts/search"
COMMENTS_URL = "https://arctic-shift.photon-reddit.com/api/comments/search"

def download(subreddit, kind="posts", start_ms=None, limit_batches=10):
    """
    kind: "posts" or "comments"
    start_ms: unix timestamp in milliseconds (or None)
    """
    url = POSTS_URL if kind == "posts" else COMMENTS_URL
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://arctic-shift.photon-reddit.com/",
    })

    after = start_ms
    batches = 0

    while True:
        if limit_batches and batches >= limit_batches:
            break

        params = {
            "subreddit": subreddit,
            "sort": "asc",
            "limit": "auto",
        }
        if after:
            params["after"] = after

        r = session.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json().get("data", [])

        if not data:
            break

        for item in data:
            print(json.dumps(item))  # one JSON per line

        # advance timestamp
        after = int(data[-1]["created_utc"] * 1000) + 1
        batches += 1
        time.sleep(1)  # be nice to the API


# Example usage
download("python", kind="posts", limit_batches=5)
# download("python", kind="comments", limit_batches=5)
