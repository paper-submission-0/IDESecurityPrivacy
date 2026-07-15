
# IDESecurityPrivacy Install Instructions

For appendix see [readme.md](https://github.com/paper-submission-0/IDESecurityPrivacy/blob/main/readme.md)

A research-oriented toolkit for collecting, processing, and analyzing Reddit discussions related to **security and privacy risks in LLM-powered IDEs (LIDEs)**.
The project supports downloading Reddit posts/comments, organizing datasets, and preparing them for further analysis such as classification, annotation, or empirical studies.

---

## 1. Environment Setup

Create and activate a Python environment from the package root:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r code/requirements.txt
```

Some scripts use local Ollama models. Start Ollama separately and pass the model name and port values at runtime.

---

## 2. Package Structure

```text
snapshot2/
├── code/
│   ├── analysis.ipynb
│   ├── comment_labeler.py
│   ├── downloader.py
│   ├── privacy_filter.py
│   ├── redditlist.txt
│   ├── requirements.txt
│   ├── security_filter.py
│   └── sentiment.py
├── data/
│   ├── comments/
│   ├── posts/
│   └── validation/
├── instructions.md
└── readme.md
```

---

## 3. Data Collection

The subreddit list is in `code/redditlist.txt`.

Download both posts and comments:

```bash
python code/downloader.py \
  --subreddits code/redditlist.txt \
  --output-dir data/raw/reddit
```

Download only posts:

```bash
python code/downloader.py \
  --subreddits code/redditlist.txt \
  --output-dir data/raw/reddit \
  --posts
```

Download only comments:

```bash
python code/downloader.py \
  --subreddits code/redditlist.txt \
  --output-dir data/raw/reddit \
  --comments
```

---

## 4. Filtering Posts

Run the security filter on a CSV file:

```bash
python code/security_filter.py \
  --input-csv INPUT.csv \
  --output-csv OUTPUT.csv \
  --model MODEL_NAME \
  --ports 11434
```

Run the privacy filter on downloaded Reddit JSONL files:

```bash
python code/privacy_filter.py \
  --root-dir data/raw/reddit \
  --output-csv OUTPUT.csv \
  --model MODEL_NAME \
  --ports 11434 \
  --subreddits code/redditlist.txt
```

Use comma-separated ports for multiple Ollama instances:

```bash
--ports 11434,11435,11436
```

---

## 5. Comment Labeling

Label comments with the mitigation-topic codebook:

```bash
python code/comment_labeler.py \
  --input-csv data/comments/all_valid_comments.csv \
  --output-csv data/comments/labeled.csv \
  --ollama-url http://localhost:11434/api/generate \
  --model MODEL_NAME
```

---

## 6. Sentiment Analysis

Run sentiment analysis on a post CSV:

```bash
python code/sentiment.py \
  --input-csv data/posts/446_posts.csv \
  --output-csv data/posts/446_posts_with_sentiment.csv \
  --model cardiffnlp/twitter-roberta-base-sentiment-latest
```

---

## 7. Notebook Analysis

Open and run:

```text
code/analysis.ipynb
```

The notebook expects the validated post dataset at:

```text
data/posts/446_posts.csv
```

Some notebook figures write PDF or PNG files into the current working directory when cells are executed.

