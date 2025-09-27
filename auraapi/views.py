import os
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET

API_ROOT = Path(__file__).resolve().parents[1]  # src/api
RAW_GROUND = API_ROOT / "data" / "raw" / "ground"
PROCESSED = API_ROOT / "data" / "processed"
OUTPUTS = API_ROOT / "outputs"


def _city_slug(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def _load_csv(path: Path):
    if not path.exists():
        return None
    try:
        return pd.read_csv(path, parse_dates=["datetime_utc"])  # normalized by teammate
    except Exception:
        return None


@require_GET
def health(request):
    return JsonResponse({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})


@require_GET
def list_cities(request):
    # Derive from available files in data/raw/ground
    cities = set()
    if RAW_GROUND.exists():
        for p in RAW_GROUND.glob("*_pm25.csv"):
            cities.add(p.stem.replace("_pm25", "").replace("_", " ").title())
        for p in RAW_GROUND.glob("*_no2.csv"):
            cities.add(p.stem.replace("_no2", "").replace("_", " ").title())
    return JsonResponse({"cities": sorted(cities)})


@require_GET
def ground_timeseries(request, city: str, param: str):
    slug = _city_slug(city)
    path = RAW_GROUND / f"{slug}_{param.lower()}.csv"
    df = _load_csv(path)
    if df is None or df.empty:
        raise Http404("No ground data found")
    # Optional date filters
    start = request.GET.get("start")
    end = request.GET.get("end")
    if start:
        df = df[df["datetime_utc"] >= pd.to_datetime(start, utc=True, errors="coerce")]
    if end:
        df = df[df["datetime_utc"] <= pd.to_datetime(end, utc=True, errors="coerce")]
    # Trim columns for API
    keep = [c for c in ["datetime_utc", "value", "unit", "location", "sensor_id", "lat", "lon"] if c in df.columns]
    rows = df.sort_values("datetime_utc")[keep].head(5000).to_dict(orient="records")
    return JsonResponse({"city": city, "param": param, "count": len(rows), "data": rows})


@require_GET
def tempo_collocated(request, city: str):
    slug = _city_slug(city)
    path_parquet = PROCESSED / f"collocated_{slug}_no2.parquet"
    path_csv = PROCESSED / f"collocated_{slug}_no2.csv"
    df = None
    if path_parquet.exists():
        try:
            df = pd.read_parquet(path_parquet)
        except Exception:
            df = None
    if df is None and path_csv.exists():
        try:
            df = pd.read_csv(path_csv, parse_dates=["datetime_utc"])
        except Exception:
            df = None
    if df is None or df.empty:
        raise Http404("No collocated data found or unreadable")
    keep = [c for c in ["datetime_utc", "sensor_id", "ground_no2", "tempo_no2", "cloud_fraction", "qa_flag", "lat", "lon"] if c in df.columns]
    rows = df.sort_values("datetime_utc")[keep].head(5000).to_dict(orient="records")
    return JsonResponse({"city": city, "count": len(rows), "data": rows})


@require_GET
def forecast(request, city: str, param: str):
    slug = _city_slug(city)
    path = OUTPUTS / f"forecast_{slug}_{param.lower()}.json"
    if not path.exists():
        raise Http404("No forecast found")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        raise Http404("Unable to parse forecast JSON")
    return JsonResponse(data)


@require_GET
def manifest(request):
    path = OUTPUTS / "manifest.json"
    if not path.exists():
        return JsonResponse({"cities": [], "params": []})
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return JsonResponse({"cities": [], "params": []})
    return JsonResponse(data)
