
SELECT
   route_id,
   origin_city,
   destination_city,
   transport_type,
   distance_km
FROM {{ source('raw', 'routes')}}