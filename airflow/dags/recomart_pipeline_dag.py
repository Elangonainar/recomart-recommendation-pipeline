from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'recomart-data-eng',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'recomart_end_to_end_pipeline',
    default_args=default_args,
    description='Automated Data Management Pipeline for RecoMart Recommendation System',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['recomart', 'mlops', 'recommendation'],
) as dag:

    ingest_clickstream = BashOperator(
        task_id='ingest_clickstream_logs',
        bash_command='python /app/ingestion/clickstream_simulator.py',
    )

    ingest_catalog = BashOperator(
        task_id='ingest_product_catalog_api',
        bash_command='python /app/ingestion/api_client.py',
    )

    validate_raw_data = BashOperator(
        task_id='validate_raw_data',
        bash_command='python /app/validation/validator.py',
    )

    prepare_data = BashOperator(
        task_id='prepare_and_clean_data',
        bash_command='python /app/preprocessing/data_prep.py',
    )

    transform_features = BashOperator(
        task_id='engineer_and_store_features',
        bash_command='python /app/transformation/transformer.py',
    )

    train_model = BashOperator(
        task_id='train_and_evaluate_svd_model',
        bash_command='python /app/models/train_recommendation.py',
    )

    [ingest_clickstream, ingest_catalog] >> validate_raw_data >> prepare_data >> transform_features >> train_model
