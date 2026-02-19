
# IDESecurityPrivacy Install Instructions

For appendix see [readme.md](https://github.com/paper-submission-0/IDESecurityPrivacy/blob/main/readme.md)

A research-oriented toolkit for collecting, processing, and analyzing Reddit discussions related to **security and privacy risks in LLM-powered IDEs (LIDEs)**.
The project supports downloading Reddit posts/comments, organizing datasets, and preparing them for further analysis such as classification, annotation, or empirical studies.

---

## 1. Environment Setup

### Install Required Packages

All required dependencies are listed in `references.txt`.

```bash
pip install -r references.txt
```

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows
```

---

## 2. Data Collection

### Use `download.py` to Download Posts or Comments

`download.py` is the primary entry point for data collection.

Typical usage:

```bash
python download.py
```

## 4. Project Structure

```
IDESecurityPrivacy/
│
├── download.py                # Entry point for downloading Reddit data
├── references.txt         # Python dependency list
├── data/                  # Downloaded posts/comments
└── README.md
```
