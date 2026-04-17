from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import sys

# Add scripts folder to path
sys.path.append('/opt/airflow/scripts')

from transform import transform_data   # ✅ import your updated script

DATA_PATH = "/opt/airflow/data/final_email_thread_dataset.csv"

# ------------------ TASK 1: INGEST ------------------
def ingest_data(**context):
    print("Reading CSV...")
    df = pd.read_csv(DATA_PATH)
    print(f"Rows loaded: {len(df)}")

    context['ti'].xcom_push(key='data', value=df.to_json())


# ------------------ TASK 2: VALIDATE ------------------
def validate_data(**context):
    print("Validating data...")

    data = context['ti'].xcom_pull(key='data')
    df = pd.read_json(data)

    expected_columns = ["thread_id", "thread_text", "summary"]

    if list(df.columns) != expected_columns:
        raise ValueError("Schema mismatch ❌")

    if df.isnull().sum().sum() > 0:
        raise ValueError("Null values found ❌")

    print("Validation passed ✅")

    context['ti'].xcom_push(key='validated_data', value=df.to_json())


# ------------------ DAG ------------------
with DAG(
    dag_id="email_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    ingest = PythonOperator(
        task_id="ingest",
        python_callable=ingest_data
    )

    validate = PythonOperator(
        task_id="validate",
        python_callable=validate_data
    )

    # ✅ NOW using your transform.py (with MinIO upload)
    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_data
    )

    ingest >> validate >> transform