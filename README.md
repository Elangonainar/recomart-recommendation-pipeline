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
