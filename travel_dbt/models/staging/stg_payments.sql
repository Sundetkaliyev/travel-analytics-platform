SELECT
   payment_id,
   order_id,
   amount,
   method,
   status,
   paid_at
FROM {{ source('raw', 'payments')}}