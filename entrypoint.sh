#!/bin/bash
set -e

echo "=== Initializing RecoMart Data Pipeline Environment ==="

if [ ! -f "airflow/airflow.db" ]; then
    echo "Initializing Airflow metadata database..."
    airflow db init
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@recomart.com \
        --password admin
fi

if [ "$1" = "all" ]; then
    echo "Starting Airflow standalone webserver and scheduler..."
    airflow standalone &
    
    echo "Running initial pipeline stages..."
    python ingestion/clickstream_simulator.py
    python ingestion/api_client.py
    python validation/validator.py
    python preprocessing/data_prep.py
    python transformation/transformer.py
    python models/train_recommendation.py
    
    wait
else
    exec "$@"
fi
