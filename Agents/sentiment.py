import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
_tokenizer = AutoTokenizer.from_pretrained(_MODEL)
_model     = AutoModelForSequenceClassification.from_pretrained(_MODEL)

_sentiment = pipeline(
    "sentiment-analysis",
    model=_model,
    tokenizer=_tokenizer,
    device=-1,
    batch_size=32
)

def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    results = _sentiment(
        df['cleaned'].tolist(),
        truncation=True,
        padding=True,
        max_length=_tokenizer.model_max_length
    )
    df['sent_label'] = [r['label'] for r in results]
    df['sent_score'] = [r['score'] for r in results]
    return df
