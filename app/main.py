import os

from fastapi import FastAPI

VERSION = "2.0.0"

app = FastAPI(title="cicd-autonomy-demo")


@app.get("/")
def root() -> dict:
    return {
        "service": "cicd-autonomy-demo",
        "version": VERSION,
        "environment": os.getenv("APP_ENV", "unknown"),
        "features": ["greeting"],
    }


@app.get("/greet")
def greet() -> dict:
    return {"greeting": "Hello from v2!"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
