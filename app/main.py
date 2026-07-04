import os

from fastapi import FastAPI

VERSION = "1.0.0"

app = FastAPI(title="cicd-autonomy-demo")


@app.get("/")
def root() -> dict:
    return {
        "service": "cicd-autonomy-demo",
        "version": VERSION,
        "environment": os.getenv("APP_ENV", "unknown"),
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
