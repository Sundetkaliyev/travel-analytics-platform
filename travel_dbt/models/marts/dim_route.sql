-- Dimension: маршруты. Строим из stg_routes.
SELECT
    route_id,
    origin_city,
    destination_city,
    transport_type,
    distance_km
FROM {{ ref('stg_routes') }}