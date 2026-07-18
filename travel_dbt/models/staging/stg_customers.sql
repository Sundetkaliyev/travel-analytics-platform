-- Staging: клиенты. Берём сырую таблицу customers и выбираем нужные колонки.
SELECT
    customer_id,
    full_name,
    email,
    city,
    registered_at
FROM {{ source('raw', 'customers') }}









