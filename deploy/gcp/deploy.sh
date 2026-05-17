#!/usr/bin/env bash
# ── Deploy Senior Dev Agent to Cloud Run ──────────────────────────────────────
# Usage: ./deploy.sh
# Prerequisites:
#   gcloud auth login
#   gcloud config set project YOUR_PROJECT_ID
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
REGION="${REGION:-us-central1}"
SERVICE_NAME="senior-dev-agent"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

echo "▶ Project : ${PROJECT_ID}"
echo "▶ Region  : ${REGION}"
echo "▶ Image   : ${IMAGE}"

# 1. Enable required APIs
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com \
  --project="${PROJECT_ID}"

# 2. Build & push image via Cloud Build
gcloud builds submit \
  --tag="${IMAGE}" \
  --project="${PROJECT_ID}" \
  ../../   # build context = repo root

# 3. Deploy to Cloud Run
gcloud run deploy "${SERVICE_NAME}" \
  --image="${IMAGE}" \
  --region="${REGION}" \
  --platform=managed \
  --allow-unauthenticated \
  --memory=4Gi \
  --cpu=2 \
  --timeout=120 \
  --set-env-vars="LLM_BACKEND=vertexai,VERTEX_PROJECT=${PROJECT_ID},VERTEX_LOCATION=${REGION},VERTEX_MODEL=gemma-3-27b-it" \
  --project="${PROJECT_ID}"

echo ""
echo "✅ Deployed! Service URL:"
gcloud run services describe "${SERVICE_NAME}" \
  --region="${REGION}" \
  --format="value(status.url)"
