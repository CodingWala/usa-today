app/
├── main.py                # entry point
├── pipeline.py            # orchestration
├── config.py              # env vars only
├── models.py              # Article dataclass / schema
│
├── sources/               # WHERE links come from
│   ├── base.py
│   ├── factory.py
│   ├── yahoo.py
│   └── newsapi.py
│
├── scraper.py             # HOW article body is extracted
│
├── nlp/                   # text intelligence
│   ├── __init__.py
│   └── gist.py
│
├── storage/               # persistence
│   ├── __init__.py
│   └── duckdb.py
│
└── utils/ (optional)
