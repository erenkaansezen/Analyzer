# pipeline.py

from Agents.scraper import scrape_app_reviews
from Agents.preprocessing import preprocess
from Agents.sentiment import analyze_sentiment
from Agents.fake_review import predict_fake
import pandas as pd
import os


def classify_sentiment(row):
    label = row['sent_label']
    if '1' in label or '2' in label:
        return 'NEGATIVE'
    elif '3' in label:
        return 'NEUTRAL'
    elif '4' in label or '5' in label:
        return 'POSITIVE'
    return 'UNKNOWN'


def detect_constructive(row):
    keywords = [
        "düzelt", "güncelle", "geliştir", "ekle", "özellik", "öneri", 
        "hata", "aksaklık", "problem", "sorun", "öner", "fix", "update", 
        "improve", "add", "feature", "suggestion", "bug", "glitch", "error", 
        "issue", "recommend"
    ]
    text = row.get('cleaned', '').lower()
    return int(any(kw in text for kw in keywords))


def run_pipeline(app_id: str, max_reviews: int = None) -> dict:

    raw = scrape_app_reviews(app_id, max_reviews=max_reviews)
    if raw.empty:
        raise RuntimeError(f" {app_id} için hiç yorum bulunamadı.")
    print(f"Scrape tamam – {len(raw)} yorum")


    prep = preprocess(raw)


    sent = analyze_sentiment(prep)


    sent = predict_fake(sent)



    sent['constructive'] = sent.apply(detect_constructive, axis=1)


    sent['sentiment'] = sent.apply(classify_sentiment, axis=1)


    sentiment_counts = sent['sentiment'].value_counts().to_dict()
    constructive_count = int(sent['constructive'].sum())
    fake_count = int(sent['fake_review'].sum())


    top_constructive_comments = (
        sent[sent['constructive'] == 1]
        .drop_duplicates(subset='cleaned')
        .sort_values(by='score', ascending=False)
        .head(100)[['cleaned', 'sentiment', 'score']]
        .rename(columns={'cleaned': 'content', 'score': 'stars'})
        .to_dict(orient='records')
    )


    top_fake_comments = (
        sent[sent['fake_review'] == 1]
        .drop_duplicates(subset='cleaned')
        .head(100)[['cleaned', 'sentiment', 'score']]
        .rename(columns={'cleaned': 'content', 'score': 'stars'})
        .to_dict(orient='records')
    )

    os.makedirs("out", exist_ok=True)
    sent.to_csv("out/final.csv", index=False, encoding='utf-8')


    return {
        "sentiment_counts": sentiment_counts,
        "constructive_comments_count": constructive_count,
        "fake_comments_count": fake_count,
        "top_constructive_comments": top_constructive_comments,
        "top_fake_comments": top_fake_comments
    }

if __name__ == "__main__":
    output = run_pipeline("com.flatgames.patrolofficer")
    print(output)
