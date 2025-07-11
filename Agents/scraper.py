import pandas as pd
import pycountry
from google_play_scraper import reviews_all, Sort
from datetime import datetime


LOCALES = [
    (lang.alpha_2, lang.alpha_2)
    for lang in pycountry.languages
    if hasattr(lang, 'alpha_2')
]

def scrape_app_reviews(app_id: str, max_reviews: int = None) -> pd.DataFrame:
    all_reviews = []
    for lang, country in LOCALES:

        batch = reviews_all(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=max_reviews
        )
        if batch:

            for r in batch:
                r["_lang"] = lang
                r["_country"] = country
            all_reviews.extend(batch)

    if not all_reviews:
        raise RuntimeError(f" {app_id} için hiç yorum bulunamadı.")
    df = pd.DataFrame(all_reviews)
    df["scrape_time"] = datetime.utcnow()

    if "content" not in df.columns and "reviewText" in df.columns:
        df = df.rename(columns={"reviewText": "content"})
    return df