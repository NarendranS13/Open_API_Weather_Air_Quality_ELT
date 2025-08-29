from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="simple_test_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["test"],
) as dag:
    
    # Task to echo a message
    echo_task = BashOperator(
        task_id="echo_message",
        bash_command='echo "This is a simple test DAG!"',
    )