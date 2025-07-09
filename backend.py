from fastapi import FastAPI
from pipeline import run_pipeline

app = FastAPI()

@app.get("/")
def root():
    return {"status": "up"}

@app.get("/analyze/{app_id}")
def analyze(app_id: str):
    return run_pipeline(app_id)
