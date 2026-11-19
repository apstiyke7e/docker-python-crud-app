import json
import random
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parent
RECORDS_PATH = BASE_DIR / "records.json"
STATIC_DIR = BASE_DIR / "static"


def load_records() -> list[dict[str, Any]]:
    with RECORDS_PATH.open(encoding="utf-8") as records_file:
        records = json.load(records_file)
    if not isinstance(records, list):
        raise ValueError("records.json must contain a JSON array")
    return records


RECORDS = load_records()
app = FastAPI(title="The Record Room", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def matching_records(q: str, category: str) -> list[dict[str, Any]]:
    query = q.strip().casefold()
    selected_category = category.strip().casefold()
    return [
        record
        for record in RECORDS
        if (not selected_category or record["category"].casefold() == selected_category)
        and (
            not query
            or query
            in " ".join(
                str(record.get(field, ""))
                for field in ("title", "description", "holder", "category")
            ).casefold()
        )
    ]


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/records")
def get_records(
    q: str = Query(default="", max_length=100),
    category: str = Query(default="", max_length=60),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=12, ge=1, le=100),
) -> dict[str, Any]:
    records = matching_records(q, category)
    return {
        "items": records[offset : offset + limit],
        "total": len(records),
        "offset": offset,
        "limit": limit,
    }


@app.get("/api/categories")
def get_categories() -> list[str]:
    return sorted({record["category"] for record in RECORDS})


@app.get("/api/random")
def get_random_record(
    q: str = Query(default="", max_length=100),
    category: str = Query(default="", max_length=60),
) -> dict[str, Any]:
    records = matching_records(q, category)
    if not records:
        raise HTTPException(status_code=404, detail="No matching records found")
    return random.choice(records)
