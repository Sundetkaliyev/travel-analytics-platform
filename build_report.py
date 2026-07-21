"""Автоматический Excel-отчёт по данным Travel Analytics (pandas -> Excel)."""
import pandas as pd

BASE = "/Users/bagdauletsundetkaliyev/travel-analytics/powerbi_data"

# Загрузка и обогащение
bookings = pd.read_csv(f"{BASE}/fact_bookings.csv")
routes   = pd.read_csv(f"{BASE}/dim_route.csv")
rfm      = pd.read_csv(f"{BASE}/rfm_segments.csv")
df = bookings.merge(routes, left_on="route_key", right_on="route_id", how="left")
paid = df[df["order_status"] == "paid"]

# Лист 1: KPI
conversion = df[df.order_status == "paid"]["order_id"].nunique() / df["order_id"].nunique() * 100
kpi = pd.DataFrame({
    "Метрика": ["Выручка, тг", "Билетов продано", "Средний чек, тг", "Конверсия, %"],
    "Значение": [round(paid["price"].sum()), len(paid),
                 round(paid["price"].mean()), round(conversion, 1)],
})

# Лист 2: выручка по транспорту
by_transport = (paid.groupby("transport_type")["price"]
                .agg(Выручка="sum", Билетов="count").reset_index())

# Лист 3: топ-10 маршрутов
top_routes = (paid.groupby(["origin_city", "destination_city"])["price"].sum()
              .reset_index().sort_values("price", ascending=False).head(10))

# Лист 4: RFM-сегменты
rfm_dist = rfm["segment"].value_counts().reset_index()
rfm_dist.columns = ["Сегмент", "Клиентов"]

# Сборка Excel-отчёта (многолистовой)
out = f"{BASE}/travel_report.xlsx"
with pd.ExcelWriter(out, engine="openpyxl") as writer:
    kpi.to_excel(writer, sheet_name="KPI", index=False)
    by_transport.to_excel(writer, sheet_name="Транспорт", index=False)
    top_routes.to_excel(writer, sheet_name="Топ маршруты", index=False)
    rfm_dist.to_excel(writer, sheet_name="RFM", index=False)

print("Готово! Отчёт:", out)
