import pandas as pd
from minio import Minio

def transform_data(**context):   # 
    print("Reading CSV...")
    df = pd.read_csv("/opt/airflow/data/final_email_thread_dataset.csv")

    print(f"Data shape: {df.shape}")

    # Schema validation
    expected_columns = ["thread_id", "thread_text", "summary"]
    if list(df.columns) != expected_columns:
        raise ValueError("Schema mismatch!")

    print("Schema validated ✅")

    # Null check
    if df.isnull().sum().sum() > 0:
        print("Warning: Null values found")

    # Transformation
    print("Processing...")
    df["text_length"] = df["thread_text"].astype(str).str.len()

    # Save locally
    file_path = "/opt/airflow/data/email_threads.parquet"
    print("Saving Parquet...")
    df.to_parquet(file_path, index=False)

    # Upload to MinIO
    print("Uploading to MinIO...")

    client = Minio(
        "minio:9000",
        access_key="admin",
        secret_key="password123",
        secure=False
    )

    bucket_name = "email-data"

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    client.fput_object(
        bucket_name,
        "email_threads.parquet",
        file_path
    )

    print("Uploaded to MinIO ✅")
    print("Pipeline completed ✅")