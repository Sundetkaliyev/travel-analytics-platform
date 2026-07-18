WITH
paid AS (
    SELECT * FROM {{ ref('fact_bookings') }} WHERE order_status = 'paid'
),
rfm_base AS (
    SELECT
        customer_key,
        MAX(date_key)            AS last_purchase,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(price)               AS monetary
    FROM paid
    GROUP BY customer_key
),
rfm_scored AS (
    SELECT
        customer_key, last_purchase, frequency, monetary,
        NTILE(5) OVER (ORDER BY monetary)      AS m_score,
        NTILE(5) OVER (ORDER BY frequency)     AS f_score,
        NTILE(5) OVER (ORDER BY last_purchase) AS r_score
    FROM rfm_base
)
SELECT
    customer_key, r_score, f_score, m_score, monetary,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN f_score >= 4 AND m_score >= 4                  THEN 'Loyal'
        WHEN r_score >= 4                                   THEN 'Recent'
        WHEN r_score <= 2 AND f_score <= 2                  THEN 'At Risk'
        ELSE 'Regular'
    END AS segment
FROM rfm_scored