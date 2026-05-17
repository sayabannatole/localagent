# Senior AI Developer Agent

An open-source LLM-powered REST API that acts as a **senior AI developer**.  
Runs locally via **Ollama** and on **GCP Cloud Run** via **Vertex AI**.

---

## Capabilities

| Endpoint | Activity |
|---|---|
| `POST /review/` | Code review with critical / major / minor feedback |
| `POST /architecture/` | Architecture design + formal ADR generation |
| `POST /pr/summarise` | PR diff summarisation + reviewer checklist |
| `POST /debug/` | Root cause analysis + fix + prevention strategy |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  FastAPI REST API                    │
│   /review   /architecture   /pr/summarise   /debug  │
└──────────────────────┬──────────────────────────────┘
                       │
                ┌──────▼──────┐
                │  BaseAgent  │  ← Senior Dev Persona + Task Prompt
                └──────┬──────┘
                       │
           ┌───────────▼───────────┐
           │     LLM Abstraction   │
           ├───────────┬───────────┤
           │  Ollama   │ Vertex AI │
           │ (local)   │  (GCP)    │
           └───────────┴───────────┘
```

**Model recommendations:**

| Environment | Model | RAM required |
|---|---|---|
| Local (8 GB) | `codellama:13b` or `deepseek-coder:6.7b` | ~6 GB |
| Local (16 GB+) | `deepseek-coder:33b` | ~20 GB (quantised) |
| GCP Vertex AI | `gemma-3-27b-it` | managed |

---

## Local Development

### 1. Install Ollama and pull a model

```bash
# Install Ollama — https://ollama.com
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model (choose based on your RAM)
ollama pull deepseek-coder:33b     # 16 GB+ RAM
# ollama pull codellama:13b        # 8 GB RAM
```

### 2. Run with Docker Compose

```bash
cd deploy/local
docker compose up --build
```

API available at `http://localhost:8000`

### 3. Run without Docker

```bash
pip install -r requirements.txt
cp .env.example .env           # edit if needed
uvicorn app.main:app --reload --port 8000
```

---

## GCP Deployment (Cloud Run + Vertex AI)

### Prerequisites

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Deploy

```bash
chmod +x deploy/gcp/deploy.sh
cd deploy/gcp && ./deploy.sh
```

This will:
1. Enable Cloud Run, Cloud Build, Artifact Registry, Vertex AI APIs
2. Build the Docker image via Cloud Build
3. Deploy to Cloud Run with Vertex AI env vars set

---

## API Usage

### Code Review

```bash
curl -X POST http://localhost:8000/review/ \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def get_user(id):\n    return db.query(f\"SELECT * FROM users WHERE id={id}\")",
    "context": "Python 3.11, FastAPI, PostgreSQL"
  }'
```

### Architecture Design + ADR

```bash
curl -X POST http://localhost:8000/architecture/ \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Design a RAG pipeline for AEM Content Fragments with semantic search",
    "context": "GCP, Python, existing AEM as Cloud Service, team of 4 engineers"
  }'
```

### PR Summary

```bash
curl -X POST http://localhost:8000/pr/summarise \
  -H "Content-Type: application/json" \
  -d '{
    "diff": "$(git diff main...feature-branch)",
    "context": "JIRA-123: Add Redis caching to user service"
  }'
```

### Debugging

```bash
curl -X POST http://localhost:8000/debug/ \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "OOMKilled — Java heap space in Spring Boot pod",
    "context": "Kubernetes 1.29, JVM 17, heap set to 512m, spike in traffic at 14:00"
  }'
```

---

## Interactive API Docs

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Running Tests

```bash
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

---

## Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `LLM_BACKEND` | `ollama` | `ollama` or `vertexai` |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `deepseek-coder:33b` | Model to use locally |
| `VERTEX_PROJECT` | _(required on GCP)_ | GCP project ID |
| `VERTEX_LOCATION` | `us-central1` | Vertex AI region |
| `VERTEX_MODEL` | `gemma-3-27b-it` | Vertex AI model |

---

## Extending the Agent

To add a new capability (e.g. `security-audit`):

1. Create `app/agents/security_audit.py` extending `BaseAgent`
2. Create `app/routes/security.py` with a FastAPI router
3. Register it in `app/main.py` with `app.include_router(...)`

The persona and base prompt chain apply automatically.

---

## Project Structure

```
senior-dev-agent/
├── app/
│   ├── main.py               # FastAPI app + lifespan
│   ├── agents/
│   │   ├── base.py           # BaseAgent + Senior Dev persona
│   │   ├── code_review.py
│   │   ├── architecture.py
│   │   ├── pr_summary.py
│   │   └── debug.py
│   ├── models/
│   │   └── llm.py            # Ollama / Vertex AI abstraction
│   └── routes/
│       ├── review.py
│       ├── architecture.py
│       ├── pr.py
│       └── debug.py
├── deploy/
│   ├── local/docker-compose.yml
│   └── gcp/deploy.sh
├── tests/test_routes.py
├── Dockerfile
├── requirements.txt
└── .env.example
```
