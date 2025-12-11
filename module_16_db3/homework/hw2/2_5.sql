SELECT DISTINCT
    c1.customer_name AS customer_1,
    c2.customer_name AS customer_2
FROM customers c1
JOIN customers c2 ON
    c1.customer_id < c2.customer_id AND
    c1.city = c2.city AND
    c1.manager_id = c2.manager_id;
