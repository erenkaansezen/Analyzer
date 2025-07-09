import pandas as pd

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['cleaned'] = (
        df['content']
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    df = df[df['cleaned'].str.len() > 0]
    return df
