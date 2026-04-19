# Email Data Pipeline (Airflow + MinIO)

##  Overview

This project implements an end-to-end **Data Engineering pipeline** using **Apache Airflow and MinIO**.

The pipeline ingests a local CSV file, validates its schema, performs transformations, and stores the processed data as **Parquet files in MinIO object storage**.

---

##  Architecture

```text
Local CSV → Airflow DAG → Validation → Transformation → Parquet → MinIO
```

---

## Tech Stack

* **Apache Airflow** – Workflow orchestration
* **Docker & Docker Compose** – Containerization
* **MinIO** – Object storage (S3-compatible)
* **Python (Pandas)** – Data processing
* **Parquet** – Efficient columnar storage

---

##  Project Structure

```
dhap42_pipeline/
│
├── dags/
│   └── email_pipeline.py        # Airflow DAG
│
├── scripts/
│   └── transform.py            # Transformation + MinIO upload
│
├── data/
│   ├── final_email_thread_dataset.csv
│   └── email_threads.parquet
│
├── docker-compose.yml
└── README.md
```

---

##  Pipeline Steps

### 1. Ingest

* Reads CSV file from local storage
* Loads data into Airflow pipeline

### 2. Validate

* Checks schema:

  * `thread_id`
  * `thread_text`
  * `summary`
* Ensures no null values
* Fails pipeline if mismatch

### 3. Transform

* Adds new feature: `text_length`
* Converts data into Parquet format

### 4. Load (MinIO)

* Uploads Parquet file to MinIO bucket
* Creates bucket if not exists

---

## ▶ How to Run

### 1. Start services

```bash
docker compose up -d
```

---

### 2. Open Airflow

```
http://localhost:8080
```

Login:

```
username: admin
password: admin
```

---

### 3. Trigger DAG

* Enable `email_pipeline`
* Click ▶ Trigger

---

### 4. Check MinIO

```
http://localhost:9001
```

Login:

```
username: admin
password: password123
```

 Bucket: `email-data`
 Output: `email_threads.parquet`

---

## Output

* Processed Parquet file stored in MinIO
* Fully automated Airflow pipeline
* Logs available for each step

---

## 📊 Key Features

✔ End-to-end data pipeline
✔ Schema validation with failure handling
✔ Dockerized reproducible setup
✔ Integration with object storage (MinIO)
✔ Scalable architecture

---

##  Future Improvements

* Partitioned Parquet storage
* Replace SQLite with Postgres
* Add logging & monitoring
* CI/CD integration

---



