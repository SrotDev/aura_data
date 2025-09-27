import json
from pathlib import Path

API_ROOT = Path(__file__).resolve().parents[1]
RAW = API_ROOT / "data" / "raw" / "ground"
PROC = API_ROOT / "data" / "processed"
OUT = API_ROOT / "outputs"


def _slug_to_city(slug: str) -> str:
    return slug.replace("_", " ").title()


def build_manifest() -> dict:
    cities = {}
    if RAW.exists():
        for p in RAW.glob("*.csv"):
            name = p.stem  # e.g., new_york_no2
            parts = name.rsplit("_", 1)
            if len(parts) != 2:
                continue
            slug, param = parts
            city = cities.setdefault(slug, {"name": _slug_to_city(slug), "slug": slug, "params": set(), "artifacts": {"ground": [], "collocated": [], "forecasts": []}})
            city["params"].add(param)
            city["artifacts"]["ground"].append(str(p).replace(str(API_ROOT) + "\\", "").replace(str(API_ROOT) + "/", ""))

    if PROC.exists():
        for p in PROC.glob("collocated_*_no2.*"):
            # accept parquet or csv
            rel = str(p).replace(str(API_ROOT) + "\\", "").replace(str(API_ROOT) + "/", "")
            name = p.stem  # collocated_new_york_no2
            slug = name.replace("collocated_", "").replace("_no2", "")
            city = cities.setdefault(slug, {"name": _slug_to_city(slug), "slug": slug, "params": set(), "artifacts": {"ground": [], "collocated": [], "forecasts": []}})
            city["params"].add("no2")
            city["artifacts"]["collocated"].append(rel)

    if OUT.exists():
        for p in OUT.glob("forecast_*_*.json"):
            rel = str(p).replace(str(API_ROOT) + "\\", "").replace(str(API_ROOT) + "/", "")
            name = p.stem  # forecast_new_york_no2
            parts = name.replace("forecast_", "").split("_")
            if len(parts) < 2:
                continue
            slug = "_".join(parts[:-1])
            param = parts[-1]
            city = cities.setdefault(slug, {"name": _slug_to_city(slug), "slug": slug, "params": set(), "artifacts": {"ground": [], "collocated": [], "forecasts": []}})
            city["params"].add(param)
            city["artifacts"]["forecasts"].append(rel)

    # finalize
    items = []
    for slug, c in sorted(cities.items()):
        c["params"] = sorted(list(c["params"]))
        items.append(c)

    return {"schema_version": 1, "cities": items}


if __name__ == "__main__":
    manifest = build_manifest()
    out_path = OUT / "manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {out_path}")
