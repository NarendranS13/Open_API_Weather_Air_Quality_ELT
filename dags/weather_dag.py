from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# 🔑 Add project root (parent of dags/) to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from scripts.main import main


# Default Arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5)

}



with DAG(
    dag_id = "weather_etl_dag",
    default_args = default_args,
    description = "Run weather & Air Quality ETL and Upload to s3",
    schedule = "@daily",
    start_date = datetime(2025, 1, 1),
    max_active_runs= 1,
    tags = ["weather","ETL"],

)as dag:

    run_etl = PythonOperator(
        task_id = "run_weather_etl",
        python_callable = main,
    )