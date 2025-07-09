# pipeline.py

from scraper import scrape_app_reviews
from preprocessing import preprocess
from sentiment import analyze_sentiment
from fake_review import predict_fake
import pandas as pd
import os

# Duygu sınıflandırma etiketleyicisi
def classify_sentiment(row):
    label = row['sent_label']
    if '1' in label or '2' in label:
        return 'NEGATIVE'
    elif '3' in label:
        return 'NEUTRAL'
    elif '4' in label or '5' in label:
        return 'POSITIVE'
    return 'UNKNOWN'

# Yapıcı/feedback yorum tespiti
def detect_constructive(row):
    keywords = [
        "düzelt", "güncelle", "geliştir", "ekle", "özellik", "öneri", 
        "hata", "aksaklık", "problem", "sorun", "öner", "fix", "update", 
        "improve", "add", "feature", "suggestion", "bug", "glitch", "error", 
        "issue", "recommend"
    ]
    text = row.get('cleaned', '').lower()
    return int(any(kw in text for kw in keywords))

# Ana pipeline fonksiyonu
def run_pipeline(app_id: str, max_reviews: int = None) -> dict:
    # 1. Yorumları scrape et
    raw = scrape_app_reviews(app_id, max_reviews=max_reviews)
    if raw.empty:
        raise RuntimeError(f"⚠️ {app_id} için hiç yorum bulunamadı.")
    print(f"✅ Scrape tamam – {len(raw)} yorum")

    # 2. Ön işlem
    prep = preprocess(raw)

    # 3. Duygu analizi
    sent = analyze_sentiment(prep)

    # 4. Sahte yorum tahmini (embedding + DBSCAN)
    sent = predict_fake(sent)
    # 'fake_review' sütunu eklenir (0/1)

    # 5. Yapıcı yorum tespiti
    sent['constructive'] = sent.apply(detect_constructive, axis=1)

    # 6. Etiketleme
    sent['sentiment'] = sent.apply(classify_sentiment, axis=1)

    # 7. Sayımlar
    sentiment_counts = sent['sentiment'].value_counts().to_dict()
    constructive_count = int(sent['constructive'].sum())
    fake_count = int(sent['fake_review'].sum())

    # 8. En çok yıldız alan ilk 100 yapıcı yorum
    top_constructive_comments = (
        sent[sent['constructive'] == 1]
        .drop_duplicates(subset='cleaned')
        .sort_values(by='score', ascending=False)
        .head(100)[['cleaned', 'sentiment', 'score']]
        .rename(columns={'cleaned': 'content', 'score': 'stars'})
        .to_dict(orient='records')
    )

    # 9. En çok sahte gibi duran (label==1) ilk 100 yorum
    top_fake_comments = (
        sent[sent['fake_review'] == 1]
        .drop_duplicates(subset='cleaned')
        .head(100)[['cleaned', 'sentiment', 'score']]
        .rename(columns={'cleaned': 'content', 'score': 'stars'})
        .to_dict(orient='records')
    )

    # 10. Sonuçları CSV'ye kaydet
    os.makedirs("out", exist_ok=True)
    sent.to_csv("out/final.csv", index=False, encoding='utf-8')

    # 11. JSON çıktısı
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
