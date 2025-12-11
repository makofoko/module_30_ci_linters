SELECT
    c.customer_name,
    o.order_id
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.manager_id IS NULL;
