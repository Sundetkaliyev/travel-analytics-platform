SELECT
   order_id,
   customer_id,
   created_at,
   status,
   channel
FROM {{ source('raw', 'orders')}}