# USA Today Data Engineering Pipeline 🇺🇸

A scalable and production-style data engineering project that ingests, transforms, and processes USA Today data using modern cloud and ETL technologies.

---

## 📌 Project Overview

This project demonstrates an end-to-end data engineering workflow involving:

- Data ingestion from external sources/APIs
- ETL/ELT data transformation pipelines
- Scalable data processing
- Cloud-native architecture
- Automated workflows
- Analytics-ready datasets

The goal of this repository is to showcase practical data engineering concepts including:
- Batch processing
- Pipeline orchestration
- Data modeling
- Transformation logic
- Data quality validation
- Modular engineering practices

---

## 🏗️ Architecture

```text
        Source/API
             │
             ▼
      Data Ingestion Layer
             │
             ▼
      Raw Data Storage
             │
             ▼
     Transformation Layer
             │
             ▼
     Curated/Processed Data
             │
             ▼
      Reporting / Analytics

## Project Structure

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
