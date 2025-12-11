SELECT customer_name
FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id FROM orders
);

SELECT c.customer_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
