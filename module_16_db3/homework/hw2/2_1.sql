SELECT
    customers.customer_name,
    sellers.seller_name,
    orders.amount,
    orders.order_date
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
JOIN sellers ON orders.seller_id = sellers.seller_id;