# Processed data contract

This folder contains cleaned, standardized, developer-friendly tables your API will serve.

File naming:
- Collocation: `collocated_<city_slug>_no2.parquet` (or `.csv` as fallback)
- Features: `features_<city_slug>_<param>.parquet`

Collocated schema (columns):
- datetime_utc: timestamp (UTC)
- sensor_id: string (ground station id)
- ground_no2: float (surface, µg/m³ or ppb; state units separately in README if converted)
- tempo_no2: float (column density per TEMPO units)
- cloud_fraction: float (0-1)
- qa_flag: int or string per product guide
- lat, lon: float of ground station

Notes:
- Keep UTC everywhere. Localize only in presentation layers.
- Prefer Parquet (float32 where possible) for size and speed.
