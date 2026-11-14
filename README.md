# RecoMart End-to-End Data Management Pipeline for Recommendation System

Complete data management pipeline for the **Data Management for Machine Learning (S1-26_DSEZG529)** Experiential Learning Assignment.

## Repository Structure

```text
recomart-recommendation-pipeline/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── dvc.yaml
├── airflow/
│   └── dags/
│       └── recomart_pipeline_dag.py
├── ingestion/
│   ├── api_client.py
│   └── clickstream_simulator.py
├── validation/
│   └── validator.py
├── preprocessing/
│   └── data_prep.py
├── transformation/
│   ├── sql/
│   │   └── create_feature_tables.sql
│   └── transformer.py
├── feature_store/
│   ├── feature_store.yaml
│   └── definitions/
│       └── feature_defs.py
├── models/
│   ├── train_recommendation.py
│   └── evaluate.py
└── docs/
    ├── problem_formulation.md
    └── data_quality_report.md
```

## Quick Start with Docker

```bash
docker-compose up --build
```
- **Airflow UI:** `http://localhost:8080` (`admin` / `admin`)
- **MLflow UI:** `http://localhost:5000`

## Architectural Overview & Detailed Pipeline Flow

The RecoMart data management platform implements modern data stack (MDS) and MLOps principles, ensuring continuous, validated, and reproducible transformation of raw behavioral logs and product catalogs into deployable recommendation models.

```text
[Web/Mobile Clickstream Logs] ──┐
                                ├──> [Raw Data Lake (Partitioned S3/Local)] ──> [Data Quality Validation (Schema & Range)] 
[Product Catalog REST API]    ──┘                     │                                              │
                                                      v                                              v
                                            [DVC Data Lineage]                            [Cleaned EDA Datasets]
                                                                                                     │
                                                                                                     v
[MLflow Model Registry] <── [SVD Model Training & Evaluation] <── [Feast Feature Store] <── [SQL Data Warehouse Transformation]
        │
        v
[Inference API & Apache Airflow Orchestration DAG]
```

## End-to-End Pipeline Stages

1. Data Ingestion (`ingestion/`)

- Clickstream Logs (`clickstream_simulator.py`): Simulates user behavioral event streams (`view`, `add_to_cart`, `purchase`, `rating`) with structured event attributes.
- Product Catalog (`api_client.py`): Fetches product metadata, pricing, and external sentiment scores from REST endpoints with exponential backoff retry mechanisms (`tenacity`).

2. Raw Data Storage (`data/raw/`)

- Stores ingested data using a partition-pruned directory layout organized by source, data type, and timestamp (`source=<src>/type=<type>/year=YYYY/month=MM/day=DD`) to maintain immutability and audit trails.

3. Data Profiling & Quality Validation (`validation/validator.py`)

- Executes automated checks across raw CSV and JSON partitions to detect schema mismatches, null keys, duplicate event IDs, and out-of-range values (e.g., ratings restricted to 1.0–5.0, prices > 0).
- Outputs an audit summary to `docs/data_quality_report.md`.

4. Data Preparation & EDA (`preprocessing/data_prep.py`)

- Deduplicates interaction logs, handles missing values, applies Label Encoding to categorical attributes (`category`), and normalizes numerical variables (`price`) using MinMax scaling.

5. Feature Engineering & Transformation (`transformation/`)

- Derives recommendation features including User Activity Frequency, Total Purchases, Item Popularity Index, and Average Item Ratings.
- Persists transformed features into Parquet files and a relational star schema data warehouse (`data/features/recomart_dw.db` via `create_feature_tables.sql`).

6. Feature Store (`feature_store/`)

- Configures Feast feature views (`feature_defs.py`) with entity keys (`user_id`, `product_id`) and TTL policies to serve consistent features for offline training and online inference.

7. Data Versioning & Lineage (`dvc.yaml`)

- Tracks pipeline stage dependencies, raw inputs, processed partitions, and model artifacts via DVC to ensure full reproducibility.

8. Model Training & Evaluation (`models/`)

- Trains a Collaborative Filtering model using Truncated SVD Matrix Factorization on the user-item interaction utility matrix (`train_recommendation.py`).
- Evaluates performance using RMSE, Precision@5, Recall@5, and NDCG@5 (`evaluate.py`), logging parameters, metrics, and model binaries to MLflow.

9. Pipeline Orchestration (`airflow/`)

- Automates end-to-end execution via an Apache Airflow DAG (`recomart_pipeline_dag.py`) chaining ingestion, validation, preparation, transformation, and model training with automated retries.

## Step-by-Step Execution & Verification

1. Build and Launch

- Run `docker-compose up --build` in the project root directory to build the container image, initialize the Airflow SQLite metadata database, create the default admin user, and run an initial end-to-end pass of all pipeline scripts.

2. Monitor Orchestration

- Open `http://localhost:8080` (`admin` / `admin`), enable the `recomart_end_to_end_pipeline` DAG, and inspect task logs or trigger manual runs.

3. Inspect Persistent Volumes

- Generated datasets, warehouse tables, reports, and model binaries persist locally via Docker volume mounts:
  - Raw Data: `./data/raw/`
  - Cleaned Data: `./data/processed/`
  - Feature Store & DW: `./data/features/`
  - Model Artifacts: `./models/artifacts/svd_model.pkl`
  - Validation Report: `./docs/data_quality_report.md`

4. Stop Services

- Run `docker-compose down` to shut down the container while preserving all local volume data.
