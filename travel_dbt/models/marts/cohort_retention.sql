WITH
paid AS (
    SELECT * FROM {{ ref('fact_bookings') }} WHERE order_status = 'paid'
),
customer_cohort AS (
    SELECT
        customer_key,
        DATE_TRUNC('month', MIN(date_key))::date AS cohort_month
    FROM paid
    GROUP BY customer_key
),
activity AS (
    SELECT
        c.cohort_month,
        c.customer_key,
        (EXTRACT(YEAR  FROM p.date_key) - EXTRACT(YEAR  FROM c.cohort_month)) * 12
          + (EXTRACT(MONTH FROM p.date_key) - EXTRACT(MONTH FROM c.cohort_month)) AS month_number
    FROM paid p
    JOIN customer_cohort c ON c.customer_key = p.customer_key
),
cohort_table AS (
    SELECT
        cohort_month,
        month_number,
        COUNT(DISTINCT customer_key) AS customers
    FROM activity
    GROUP BY cohort_month, month_number
)
SELECT
    cohort_month,
    month_number,
    customers,
    ROUND(
        100.0 * customers
        / FIRST_VALUE(customers) OVER (PARTITION BY cohort_month ORDER BY month_number),
        1
    ) AS retention_pct
FROM cohort_table