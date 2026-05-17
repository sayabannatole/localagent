"""
Integration tests — uses a mock LLM so no real model is needed.
Run: pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock


# ── Patch LLM before importing app ───────────────────────────────────────────
import app.models.llm as llm_module

_mock_llm = MagicMock()
_mock_llm.chat.return_value = "## Mock Response\nThis is a test response from the mock LLM."
llm_module.init_llm = lambda: _mock_llm

from app.main import app  # noqa: E402 — must import after patch

client = TestClient(app)


# ── Health ────────────────────────────────────────────────────────────────────
def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── Code Review ───────────────────────────────────────────────────────────────
def test_code_review():
    r = client.post("/review/", json={
        "code": "def add(a, b):\n    return a + b",
        "context": "Python 3.11, production service"
    })
    assert r.status_code == 200
    assert "result" in r.json()


def test_code_review_no_context():
    r = client.post("/review/", json={"code": "x = 1"})
    assert r.status_code == 200


# ── Architecture ──────────────────────────────────────────────────────────────
def test_architecture():
    r = client.post("/architecture/", json={
        "problem": "Design a RAG pipeline for AEM Content Fragments",
        "context": "GCP, Python, Vertex AI"
    })
    assert r.status_code == 200
    assert "result" in r.json()


# ── PR Summary ────────────────────────────────────────────────────────────────
def test_pr_summary():
    r = client.post("/pr/summarise", json={
        "diff": "+def new_feature():\n+    pass",
        "context": "Feature: add caching layer"
    })
    assert r.status_code == 200
    assert "result" in r.json()


# ── Debug ─────────────────────────────────────────────────────────────────────
def test_debug():
    r = client.post("/debug/", json={
        "problem": "NullPointerException at line 42",
        "context": "Java 17, Spring Boot 3.2"
    })
    assert r.status_code == 200
    assert "result" in r.json()
