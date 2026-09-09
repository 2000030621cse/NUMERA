# NUMERA — Cloud Run deploy (single service)

One container serves the Vite SPA and FastAPI on the same origin (`/api`, `/health`).

## Prerequisites

- `gcloud` CLI authenticated
- GCP project with billing
- (Optional) Gemini API key in Secret Manager

## Enable APIs

```bash
gcloud config set project YOUR_GCP_PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com
```

## Optional: Gemini secret

```bash
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets create gemini-api-key --data-file=-
```

Grant the Cloud Run runtime service account Secret Manager access if needed:

```bash
PROJECT_NUMBER=$(gcloud projects describe YOUR_GCP_PROJECT_ID --format='value(projectNumber)')
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## Deploy

From the repository root:

```bash
gcloud run deploy numera \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60 \
  --max-instances 10 \
  --set-secrets "GEMINI_API_KEY=gemini-api-key:latest" \
  --set-env-vars "GEMINI_MODEL=gemini-2.0-flash"
```

Without Gemini (deterministic fallbacks only), omit `--set-secrets`.

## Verify

```bash
curl https://YOUR-SERVICE-URL.run.app/health
```

Open the same base URL in a browser — UI and `/api` share that origin.

## Environment variables

| Variable | Required | Notes |
|----------|----------|-------|
| `PORT` | Injected by Cloud Run | Do not hardcode |
| `GEMINI_API_KEY` | Optional | Enables AI enrichment |
| `GEMINI_MODEL` | Optional | Default `gemini-2.0-flash` |
| `CORS_ORIGINS` | Optional | Comma-separated; defaults to local Vite origins |
| `STATIC_DIR` | Optional | Defaults to `/app/static` in the image |

## Local Docker smoke test

```bash
docker build -t numera .
docker run --rm -p 8080:8080 -e GEMINI_API_KEY= numera
curl http://localhost:8080/health
```
