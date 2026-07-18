-- Fact: бронирования. Зерно = 1 билет.
-- Соединяем билеты с заказами, чтобы добавить клиента и статус.
SELECT
    t.ticket_id     AS booking_id,
    t.order_id,
    o.customer_id   AS customer_key,
    t.route_id      AS route_key,
    t.travel_date   AS date_key,
    t.seat_class,
    o.status        AS order_status,
    t.price,
    1               AS ticket_count
FROM {{ ref('stg_tickets') }} AS t
JOIN {{ ref('stg_orders') }} AS o ON o.order_id = t.order_id