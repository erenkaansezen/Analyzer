import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def score_interesting(df: pd.DataFrame) -> pd.DataFrame:
    embeddings = embedder.encode(df["content"], batch_size=32)
    mean_emb = np.mean(embeddings, axis=0)
    distances = np.linalg.norm(embeddings - mean_emb, axis=1)
    df["interesting_score"] = distances.round(3)
    return df
