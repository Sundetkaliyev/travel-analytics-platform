# Airflow — оркестрация ETL

DAG `dags/travel_pipeline.py` автоматизирует ежедневный пайплайн:

    generate_data  ->  dbt_run  ->  dbt_test

## Задачи (tasks)
- **generate_data** — генерация свежих данных (Python) и загрузка в PostgreSQL
- **dbt_run** — сборка витрин (staging + DWH)
- **dbt_test** — проверка качества данных

Расписание: `@daily`. Задачи идут строго по порядку (зависимости `>>`);
при сбое следующие не стартуют, есть 1 повтор (`retries`).

## Как запустить локально
1. Создать окружение с Python 3.11 и установить Apache Airflow
2. Положить `travel_pipeline.py` в папку DAGs
3. Запустить `airflow standalone`
4. Включить DAG `travel_analytics_pipeline` в веб-интерфейсе

## Продакшн-подход (как в реальной команде)
- **Astronomer Cosmos** — каждая dbt-модель как отдельная задача Airflow
- Креды и пути через **Airflow Connections / Variables**
- **Alerting** в Slack/email при сбоях, SLA и data-freshness проверки
