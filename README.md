# Data pipeline

## Folder structure
```
data-pipeline/
├── .venv                            # virtual env
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Lint, test, type-check
│       ├── cd.yml                    # Docker build & push
│       └── data-quality.yml          # Scheduled data validation
│
├── docker/
│   ├── docker-compose.yml            # All services (Prefect, DuckDB, etc.)
│   ├── Dockerfile.ingestion          # Crawler service
│   ├── Dockerfile.pipeline           # Processing service
│   └── Dockerfile.api                # FastAPI serving service
│
├── src/
│   └── generation/                   # Data generation (for testing)
│       └── init.py
|
│   ├── ingestion/                    # LAYER 1: Data Ingestion
│   │   ├── init.py
│   │   ├── base.py                   # Abstract base crawler
│   │   ├── api_crawler.py            # REST/GraphQL API fetcher
│   │   ├── web_scraper.py            # Playwright-based scraper
│   │   ├── file_watcher.py           # Watch local files (CSV, Excel, JSON)
│   │   ├── db_connector.py           # SQLite, DuckDB, PostgreSQL
│   │   └── kaggle_downloader.py      # Kaggle dataset fetcher
│   │
│   ├── storage/                      # LAYER 2: Data Lake
│   │   ├── init.py
│   │   ├── lake.py                   # Data lake manager (Parquet/Delta)
│   │   ├── metadata.py               # Catalog & lineage tracking
│   │   └── partition.py              # Date-based partitioning logic
│   │
│   ├── preprocessing/                # LAYER 3 & 4: Transform
│   │   ├── init.py
│   │   ├── base.py
│   │   ├── null_handler.py
│   │   ├── type_converter.py
│   │   └── deduplicator.py
│   │
│   ├── validation/                   # Data Quality
│   │   │   ├── init.py
│   │   │   ├── schema_validator.py   # Pandera schemas
│   │   │   ├── custom_checks.py      # Business rules
│   │   │   └── report_generator.py   # HTML/PDF validation reports
│   │   │
│   │   └── transformation/           # Business logic
│   │       ├── init.py
│   │       ├── polars_engine.py      # High-speed transforms
│   │       ├── duckdb_engine.py      # SQL transforms
│   │       └── aggregations.py
│   │
│   ├── serving/                      # LAYER 5: Export & API
│   │   ├── init.py
│   │   ├── api/
│   │   │   ├── init.py
│   │   │   ├── main.py               # FastAPI app
│   │   │   ├── routes/
│   │   │   └── models/
│   │   ├── exporters/
│   │   │   ├── init.py
│   │   │   ├── parquet_exporter.py
│   │   │   ├── csv_exporter.py
│   │   │   ├── sqlite_exporter.py
│   │   │   └── db_loader.py
│   │   └── generators/               # Data generation (your existing tool)
│   │       └── init.py
│   │
│   └── orchestration/                # Prefect Flows
│       ├── init.py
│       ├── flows.py                  # Main pipeline DAGs
│       ├── tasks.py                  # Reusable task definitions
│       └── schedules.py              # Cron schedules
│
├── tests/
│   ├── unit/                         # Pytest unit tests
│   ├── e2e/                          # End-to-end pipeline tests
│   ├── integration/                  # Integration tests
|   └── conftest.py                   # Pytest fixtures
│
├── docs/                             # Documents
|
├── utils/
│   ├── config.py                     # Pydantic settings (env vars)
│   └── logger.py                     # Structured logging (structlog)
│   └── exceptions.py                 # Custom exceptions
├── notebooks/                        # Exploratory analysis
|
├── scripts/                          # One-off scripts
|
├── configs/                          # YAML configs per environment
│   ├── settings.py                   # Pydantic BaseSettings, reads .env
│   └── sources.yaml                  # declarative source registry
│   └── constants.py                  # Existing: Role enums, status codes
├── data/                             # Local data (gitignored)
│   ├── raw/                          # Bronze layer
│   ├── preprocessed/                 # Silver layer
│   ├── validated/                    # Validated data
|   ├── test/                         # Test data
│   ├── transformed/                  # Gold layer
│   └── quarantine/                   # Invalid data
│
├── logs/                             # Application logs
├── reports/                          # Validation reports
├── pyproject.toml                    # Poetry/UV dependencies
├── Makefile                          # Common commands
├── .env
├── .gitignore
└── README.md
```