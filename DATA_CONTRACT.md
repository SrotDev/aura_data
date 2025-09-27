# Aura API Data Contract

This document describes the expected files the API will serve and their schemas. Your data science outputs should match this to ensure smooth integration.

## Folder conventions
- Ground: `data/raw/ground/<city_slug>_<param>.csv`
- Collocated: `data/processed/collocated_<city_slug>_no2.parquet` (or `.csv` fallback)
- Features: `data/processed/features_<city_slug>_<param>.parquet`
- Forecasts: `outputs/forecast_<city_slug>_<param>.json`
- Manifest: `outputs/manifest.json`

## Ground CSV schema
- Columns (subset allowed): `datetime_utc, value, unit, location, sensor_id, lat, lon`
- Types: `datetime_utc` ISO; `value` float; `unit` string; others strings/floats
- Notes: De-duplicate by `sensor_id + datetime_utc`; ensure UTC.

## Collocated schema (Parquet preferred)
- Columns: `datetime_utc, sensor_id, ground_no2, tempo_no2, cloud_fraction, qa_flag, lat, lon`
- Types: timestamp, string, floats, int/string (qa_flag)

## Forecast JSON schema
```
{
  "city": "New York",
  "param": "no2",
  "generated_at_utc": "2025-09-27T05:30:00Z",
  "horizon_hours": 24,
  "forecasts": [
    { "datetime_utc": "2025-09-27T06:00:00Z", "yhat": 18.2, "yhat_lower": 12.1, "yhat_upper": 24.3 }
  ]
}
```

## Manifest schema
```
{
  "schema_version": 1,
  "cities": [
    {
      "name": "New York",
      "slug": "new_york",
      "params": ["pm25", "no2"],
      "artifacts": {
        "ground": ["data/raw/ground/new_york_no2.csv"],
        "collocated": ["data/processed/collocated_new_york_no2.parquet"],
        "forecasts": ["outputs/forecast_new_york_no2.json"]
      }
    }
  ]
}
```

## General rules
- Always UTC for timestamps.
- Be explicit with units (µg/m³, ppb, or TEMPO units) in README when conversions occur.
- Prefer Parquet for large internal tables; CSV is fine for ground raw outputs.
