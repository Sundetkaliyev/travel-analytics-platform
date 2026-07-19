-- ============================================================
--  Оптимизация SQL: индекс на orders.customer_id
-- ============================================================
--
--  Задача: быстро находить заказы одного клиента среди 50 000.
--
--  БЫЛО (без индекса):
--    Seq Scan on orders  -- читает все 50 000 строк
--    Rows Removed by Filter: 49992
--    Execution Time: ~32 ms
--
--  СТАЛО (с индексом):
--    Bitmap Index Scan on idx_orders_customer_id
--    Execution Time: ~0.5 ms
--
--  Результат: ускорение примерно в 58 раз.
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);

-- Проверка плана до/после:
-- EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 250;
