"""
Senior AI Developer Agent — FastAPI entrypoint.
Runs locally via Ollama or on GCP via Cloud Run (Vertex AI / Ollama sidecar).
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import review, architecture, pr, debug
from app.models.llm import init_llm


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise the LLM client on startup."""
    app.state.llm = init_llm()
    yield


app = FastAPI(
    title="Senior Dev Agent",
    description="Open-source LLM agent acting as a senior AI developer.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review.router,       prefix="/review",       tags=["Code Review"])
app.include_router(architecture.router, prefix="/architecture", tags=["Architecture"])
app.include_router(pr.router,           prefix="/pr",           tags=["PR Summary"])
app.include_router(debug.router,        prefix="/debug",        tags=["Debugging"])


@app.get("/health")
async def health():
    return {"status": "ok", "backend": os.getenv("LLM_BACKEND", "ollama")}
