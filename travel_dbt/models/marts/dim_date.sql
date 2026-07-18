-- Dimension: календарь. Генерируем по строке на каждый день.
SELECT
    d::date                          AS date_day,
    EXTRACT(YEAR    FROM d)::int      AS year,
    EXTRACT(MONTH   FROM d)::int      AS month,
    EXTRACT(QUARTER FROM d)::int      AS quarter,
    EXTRACT(DOW     FROM d)::int      AS day_of_week,   -- 0=воскресенье
    TRIM(TO_CHAR(d, 'Day'))          AS day_name
FROM generate_series(
    '2022-01-01'::date,   -- с какой даты
    '2027-12-31'::date,   -- по какую
    interval '1 day'      -- шаг = 1 день
) AS d