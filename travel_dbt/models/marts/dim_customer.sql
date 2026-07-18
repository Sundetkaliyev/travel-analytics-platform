-- Dimension: клиенты. Строим из staging-модели stg_customers.
SELECT
    customer_id,
    full_name,
    email,
    city,
    registered_at
FROM {{ ref('stg_customers') }}