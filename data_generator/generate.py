import random
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import execute_values
from faker import Faker

DB = dict(host="localhost", port=5433, dbname="travel",
          user="analyst", password="analyst_pwd")

N_CUSTOMERS = 10_000
N_ORDERS = 50_000

random.seed(42)
fake = Faker("ru_RU")
Faker.seed(42)

CITIES = ["Алматы", "Астана", "Шымкент", "Караганда", "Актобе", "Тараз",
          "Павлодар", "Усть-Каменогорск", "Атырау", "Костанай", "Кызылорда",
          "Москва", "Санкт-Петербург", "Ташкент", "Бишкек", "Дубай", "Стамбул"]

METHODS = ["card", "kaspi", "wallet"]
CHANNELS = ["web", "app"]
SEAT_CLASSES = ["economy", "business"]


def make_routes():
    routes, seen = [], set()
    while len(routes) < 60:
        a, b = random.sample(CITIES, 2)
        if (a, b) in seen:
            continue
        seen.add((a, b))
        transport = random.choice(["avia", "avia", "rail"])
        routes.append((a, b, transport, random.randint(300, 4000)))
    return routes


def seasonal_date():
    d = datetime.now() - timedelta(days=random.randint(0, 730))
    if d.month in (6, 7, 8, 12):
        return d
    if random.random() < 0.5:
        return seasonal_date()
    return d


def price_for(distance, transport, seat_class):
    base = distance * (12 if transport == "avia" else 4)
    base *= random.uniform(0.8, 1.3)
    if seat_class == "business":
        base *= 2.5
    return round(base, 2)


def main():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    cur.execute("TRUNCATE payments, tickets, orders, routes, customers "
                "RESTART IDENTITY CASCADE;")

    print("Клиенты...")
    customers = [(fake.name(), fake.unique.email(), random.choice(CITIES),
                  datetime.now() - timedelta(days=random.randint(0, 1000)))
                 for _ in range(N_CUSTOMERS)]
    customer_ids = [r[0] for r in execute_values(cur,
        "INSERT INTO customers (full_name, email, city, registered_at) "
        "VALUES %s RETURNING customer_id", customers, fetch=True)]

    print("Маршруты...")
    route_info = {}
    for rid, tr, dist in execute_values(cur,
        "INSERT INTO routes (origin_city, destination_city, transport_type, distance_km) "
        "VALUES %s RETURNING route_id, transport_type, distance_km",
        make_routes(), fetch=True):
        route_info[rid] = (tr, dist)
    route_ids = list(route_info.keys())

    print("Заказы...")
    orders = [(random.choice(customer_ids), seasonal_date(),
               random.choices(["paid", "created", "cancelled"], weights=[70, 20, 10])[0],
               random.choice(CHANNELS)) for _ in range(N_ORDERS)]
    order_rows = execute_values(cur,
        "INSERT INTO orders (customer_id, created_at, status, channel) "
        "VALUES %s RETURNING order_id, created_at, status", orders, fetch=True)

    print("Билеты и платежи...")
    tickets, payments = [], []
    for order_id, created_at, status in order_rows:
        total = 0
        for _ in range(random.choices([1, 2, 3], weights=[70, 25, 5])[0]):
            rid = random.choice(route_ids)
            tr, dist = route_info[rid]
            seat = random.choices(SEAT_CLASSES, weights=[80, 20])[0]
            price = price_for(dist, tr, seat)
            total += price
            travel = (created_at + timedelta(days=random.randint(1, 60))).date()
            tickets.append((order_id, rid, travel, price, seat))
        if status == "paid":
            payments.append((order_id, round(total, 2), random.choice(METHODS),
                             "success", created_at + timedelta(minutes=random.randint(1, 30))))
        elif status == "created":
            payments.append((order_id, round(total, 2), random.choice(METHODS),
                             random.choice(["pending", "failed"]), None))

    execute_values(cur, "INSERT INTO tickets (order_id, route_id, travel_date, price, seat_class) VALUES %s", tickets)
    execute_values(cur, "INSERT INTO payments (order_id, amount, method, status, paid_at) VALUES %s", payments)

    conn.commit()
    cur.close()
    conn.close()
    print(f"\nГотово! клиентов={len(customers)}, маршрутов=60, "
          f"заказов={len(orders)}, билетов={len(tickets)}, платежей={len(payments)}")


if __name__ == "__main__":
    main()
