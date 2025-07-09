from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import pandas as pd

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def predict_fake(df: pd.DataFrame) -> pd.DataFrame:
    embeddings = embedder.encode(df["content"], batch_size=32)
    clusters = DBSCAN(eps=0.2, min_samples=5).fit(embeddings)
    df["fake_review"] = (clusters.labels_ == -1).astype(int)
    return df
