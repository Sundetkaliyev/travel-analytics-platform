"""
Airflow DAG: ежедневный ETL для Travel Analytics Platform.

Оркеструет пайплайн: генерация данных -> dbt run -> dbt test
Запускается по расписанию @daily. Если шаг падает, следующие не стартуют.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/Users/bagdauletsundetkaliyev/travel-analytics"
DBT_DIR = f"{PROJECT_DIR}/travel_dbt"

default_args = {
    "owner": "analyst",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="travel_analytics_pipeline",
    description="Ежедневный ETL: generate -> dbt run -> dbt test",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["travel", "dbt", "etl"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command=f"cd {PROJECT_DIR} && python data_generator/generate.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test",
    )

    generate_data >> dbt_run >> dbt_test
