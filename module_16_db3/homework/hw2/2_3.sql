SELECT
    o.order_id,
    s.seller_name,
    c.customer_name
FROM orders o
JOIN sellers s ON o.seller_id = s.seller_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE s.city != c.city;