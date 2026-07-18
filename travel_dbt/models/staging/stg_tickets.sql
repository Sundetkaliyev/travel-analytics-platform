SELECT
   ticket_id,
   order_id,
   route_id,
   travel_date,
   price,
   seat_class
FROM {{source('raw', 'tickets')}}