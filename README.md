# Aura API (Django REST)

This Django project serves your teammate's prepared data to the frontend/backends.

## Endpoints

Base path: `/api/`

- `GET /api/health`
  - Simple health check.
- `GET /api/cities`
  - Lists cities derived from files in `data/raw/ground/`.
- `GET /api/ground/<city>/<param>?start=...&end=...`
  - Returns the ground time series for a city and parameter (`pm25` or `no2`).
  - Optional `start` and `end` (ISO 8601) filter the time window.
- `GET /api/tempo/<city>`
  - Collocated TEMPO vs ground for the city.
- `GET /api/forecast/<city>/<param>`
  - Returns the latest forecast JSON saved by the modeling step.
- `GET /api/manifest`
  - Summary manifest (`outputs/manifest.json`) with available artifacts.

## Project layout

- `src/api/manage.py` — Django runner
- `src/api/aura/` — project settings/urls/wsgi
- `src/api/auraapi/` — API app with views and routes

The API reads files relative to the repo root:
- `data/raw/ground/*.csv`
- `data/processed/*.parquet`
- `outputs/*.json`

## Setup and run (Windows, PowerShell)

1) Install dependencies (in your venv):
```powershell
pip install -r .\requirements.txt
```

2) Run migrations and start server:
```powershell
python -u .\src\api\manage.py migrate
python -u .\src\api\manage.py runserver 0.0.0.0:8000
```

3) Try it:
- http://127.0.0.1:8000/api/health
- http://127.0.0.1:8000/api/cities
- http://127.0.0.1:8000/api/ground/New%20York/no2
- http://127.0.0.1:8000/api/tempo/New%20York
- http://127.0.0.1:8000/api/forecast/New%20York/no2

## CORS

`django-cors-headers` allows all origins by default in dev (configured in settings). Adjust in prod with `DJANGO_ALLOWED_HOSTS` and proper CORS settings.

## Notes

- The API is filesystem-backed. Ensure your teammate’s outputs follow the folder conventions.
- If a file is missing, endpoints return HTTP 404.
