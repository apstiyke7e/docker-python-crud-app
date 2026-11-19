# The Record Room

A small FastAPI app for browsing, searching, and randomly discovering curious record-style entries. The included collection is original demo content, not official or Guinness World Records.

## Run with Docker

From this directory:

```bash
docker compose up --build
```

Then open [http://localhost:8000](http://localhost:8000). Stop the app with `Ctrl+C`; run `docker compose down` to remove its container.

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open [http://localhost:8000](http://localhost:8000). Interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

## API

- `GET /api/records?q=paper&category=Creative&offset=0&limit=12` — search and filter the collection.
- `GET /api/categories` — list available categories.
- `GET /api/random?q=paper&category=Creative` — choose a random matching entry.

To display official Guinness World Records, replace `records.json` with data you are authorized to use. Each item should include `id`, `title`, `category`, `holder`, `value`, `description`, and `icon`. The demo records are not official claims and the app is not affiliated with Guinness World Records.
