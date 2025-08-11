from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os


# Default Arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5)

}

## Path to your project folder in wsl

PROJECT_DIR = "/mnt/e/weather_api_project"
VENV_PYTHON = f"{PROJECT_DIR}/wsl_venv/bin/python"

with DAG(
    dag_id = "weather_etl_dag",
    default_args = default_args,
    description = "Run weather & Air Quality ETL and Upload to s3",
    schedule_interval = "@daily",
    start_date = datetime(2025, 1, 1),
    catchup = False,
    max_active_runs= 1,
    tags = ["weather","ETL"],

)as dag:

    run_etl = BashOperator(
        task_id = "run_weather_etl",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PYTHON} main.py"
    )