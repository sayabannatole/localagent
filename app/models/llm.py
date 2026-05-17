"""
LLM abstraction layer.
  - Local  → Ollama (codellama:13b or deepseek-coder:33b)
  - GCP    → Vertex AI (gemma-3-27b-it or code-bison)

Set env vars to control behaviour:
  LLM_BACKEND  = "ollama" | "vertexai"
  OLLAMA_HOST  = http://localhost:11434  (default)
  VERTEX_PROJECT, VERTEX_LOCATION, VERTEX_MODEL
"""
import os
from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMClient(Protocol):
    def chat(self, system: str, user: str) -> str: ...


# ── Ollama ────────────────────────────────────────────────────────────────────
class OllamaClient:
    def __init__(self):
        import ollama  # pip install ollama

        self._client = ollama
        self.model = os.getenv("OLLAMA_MODEL", "deepseek-coder:33b")
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        os.environ.setdefault("OLLAMA_HOST", host)

    def chat(self, system: str, user: str) -> str:
        response = self._client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
        )
        return response["message"]["content"]


# ── Vertex AI ─────────────────────────────────────────────────────────────────
class VertexAIClient:
    def __init__(self):
        import vertexai  # pip install google-cloud-aiplatform
        from vertexai.generative_models import GenerativeModel

        project  = os.environ["VERTEX_PROJECT"]
        location = os.getenv("VERTEX_LOCATION", "us-central1")
        model_id = os.getenv("VERTEX_MODEL", "gemma-3-27b-it")

        vertexai.init(project=project, location=location)
        self._model = GenerativeModel(model_id)

    def chat(self, system: str, user: str) -> str:
        prompt = f"{system}\n\n{user}"
        response = self._model.generate_content(prompt)
        return response.text


# ── Factory ───────────────────────────────────────────────────────────────────
def init_llm() -> LLMClient:
    backend = os.getenv("LLM_BACKEND", "ollama").lower()
    if backend == "vertexai":
        print("[LLM] Using Vertex AI backend")
        return VertexAIClient()
    print("[LLM] Using Ollama backend")
    return OllamaClient()
