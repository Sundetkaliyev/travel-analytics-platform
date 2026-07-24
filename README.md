# ✈️ Travel Analytics Platform

End-to-end аналитическая платформа для TravelTech-сервиса продажи авиа- и ж/д билетов.
Полный конвейер данных: от генерации сырых данных до DWH, витрин и сегментации клиентов.

## Технологический стек

| Слой | Инструмент |
|------|-----------|
| Хранилище данных | PostgreSQL 16 (Docker) |
| Генерация данных | Python (Faker, psycopg2) |
| Трансформации / DWH | dbt (staging, marts, тесты, документация) |
| Оркестрация | Airflow (в разработке) |
| BI | Power BI (в разработке) |

## Архитектура

RAW (сырьё) -> staging (очистка) -> marts (звёздная схема) -> аналитические витрины

## Что демонстрирует проект

- Проектирование DWH по звёздной схеме (методология Кимбалла)
- dbt: модели staging/marts, тесты качества данных (not_null, unique, relationships), автодокументация
- Продвинутый SQL: CTE, оконные функции (RANK, NTILE, FIRST_VALUE), работа с датами
- Перевод данных в бизнес-выводы

## Модель данных

- fact_bookings — факт бронирований (зерно = 1 билет)
- dim_customer, dim_route, dim_date — измерения

## Ключевые аналитические витрины

- rfm_segments — RFM-сегментация клиентов (Champions / Loyal / At Risk)
- cohort_retention — когортный анализ удержания по месяцам

## Найденные бизнес-инсайты

- Конверсия в оплату ~70% (30% заказов не доходят до оплаты)
- 28% клиентов в зоне риска (RFM) — крупнейший сегмент
- Удержание 1-го месяца ~34%

## Как запустить

docker compose up -d
python data_generator/generate.py
cd travel_dbt && dbt run && dbt test

## Структура проекта

- docker-compose.yml — PostgreSQL
- data_generator/ — генерация данных (Python)
- travel_dbt/models/staging/ — очистка сырых таблиц
- travel_dbt/models/marts/ — DWH + аналитические витрины


## Дашборд
![Выручка](<img width="1124" height="606" alt="IMAGE 2026-07-24 22_35_06" src="https://github.com/user-attachments/assets/37f02e81-9de6-4c7e-8bef-952ab0ae07dd" />
)
![RFM](<img width="1146" height="594" alt="IMAGE 2026-07-24 22_36_01" src="https://github.com/user-attachments/assets/39379bea-bd2f-4d4b-943f-31b8147fe1cc" />
)
![Когорты](<img width="1148" height="594" alt="IMAGE 2026-07-24 22_36_25" src="https://github.com/user-attachments/assets/5a15a4fa-496a-4c8e-8487-d12af3f12e9d" />)
