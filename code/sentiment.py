#!/usr/bin/env python3

import argparse

import pandas as pd
from scipy.special import softmax
from tqdm import tqdm
from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer


def preprocess(text):
    if pd.isna(text) or not isinstance(text, str):
        return ""
    parts = []
    for token in text.split(" "):
        if token.startswith("@") and len(token) > 1:
            parts.append("@user")
        elif token.startswith("http"):
            parts.append("http")
        else:
            parts.append(token)
    return " ".join(parts)


class SentimentAnalyzer:
    def __init__(self, model):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.config = AutoConfig.from_pretrained(model)
        self.model = AutoModelForSequenceClassification.from_pretrained(model)

    def analyze_text(self, text):
        if not text or pd.isna(text):
            return {label: 0.0 for label in self.config.id2label.values()}

        encoded = self.tokenizer(
            preprocess(text),
            return_tensors="pt",
            truncation=True,
            max_length=512,
        )
        output = self.model(**encoded)
        scores = softmax(output[0][0].detach().numpy())
        return {
            label: float(scores[index])
            for index, label in self.config.id2label.items()
        }

    @staticmethod
    def compound_score(scores):
        return scores.get("positive", 0.0) - scores.get("negative", 0.0)

    def analyze_dataframe(self, df, text_column):
        results = []
        for _, row in tqdm(df.iterrows(), total=len(df)):
            results.append(self.analyze_text(row.get(text_column, "")))

        for label in self.config.id2label.values():
            df[f"sentiment_{label.lower()}"] = [result.get(label, 0.0) for result in results]

        df["sentiment_label"] = [max(result, key=result.get) for result in results]
        df["sentiment_score"] = [result[max(result, key=result.get)] for result in results]
        df["sentiment_compound"] = [self.compound_score(result) for result in results]
        return df


def build_text_column(df, text_column, title_column, body_column):
    if text_column in df.columns:
        return text_column

    df[text_column] = (
        df.get(title_column, pd.Series("", index=df.index)).fillna("").astype(str)
        + "\n"
        + df.get(body_column, pd.Series("", index=df.index)).fillna("").astype(str)
    )
    return text_column


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--title-column", default="title")
    parser.add_argument("--body-column", default="selftext")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    text_column = build_text_column(
        df,
        args.text_column,
        args.title_column,
        args.body_column,
    )
    analyzer = SentimentAnalyzer(args.model)
    analyzer.analyze_dataframe(df, text_column).to_csv(args.output_csv, index=False)
    print(f"Saved results to: {args.output_csv}")


if __name__ == "__main__":
    main()
