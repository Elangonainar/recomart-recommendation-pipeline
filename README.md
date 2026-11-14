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
