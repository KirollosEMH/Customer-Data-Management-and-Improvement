ALTER TABLE Orders
Alter COLUMN order_purchase_timestamp DATETIME;

ALTER TABLE Orders
Alter COLUMN order_delivered_customer_date DATETIME;

ALTER TABLE Orders
Alter COLUMN order_delivered_carrier_date DATETIME;

ALTER TABLE Orders
Alter COLUMN order_estimated_delivery_date DATETIME;

ALTER TABLE Orders
Alter COLUMN order_approved_at DATETIME;


-- 1. Extract customer details along with their order history
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       o.order_id, o.order_status, o.order_purchase_timestamp,
       o.order_delivered_customer_date
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
ORDER BY o.order_purchase_timestamp DESC;

-- 2. Count the number of orders per customer
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       COUNT(o.order_id) AS total_orders
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_first_name, c.customer_last_name
ORDER BY total_orders DESC;

-- 3. Find customers who have given the highest review scores
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       r.review_score
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
JOIN OrderReviews AS r
ON o.order_id = r.order_id
WHERE r.review_score between 4 and 5 order by r.review_score desc;

-- 4. Update customer phone numbers
UPDATE Customers
SET customer_phone = '1234567890'
WHERE customer_id = '06b8999e2fba1a1fbc88172c00ba8bc7';

-- 5. Calculate total payment made by each customer
SELECT c.customer_id, c.customer_first_name, c.customer_last_name,
       SUM(p.payment_value) AS total_payment
FROM Customers AS c
JOIN orders AS o
ON c.customer_id = o.customer_id
JOIN OrderPayments AS p
ON o.order_id = p.order_id
GROUP BY c.customer_id, c.customer_first_name, c.customer_last_name
ORDER BY total_payment DESC;

-- 6. List customers from a specific state with their order status
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       c.customer_state, o.order_status
FROM Customers AS c
JOIN orders AS o
ON c.customer_id = o.customer_id
WHERE c.customer_state = 'SC';

-- 7. Find customers who have delayed deliveries
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       o.order_id, o.order_estimated_delivery_date, 
       o.order_delivered_customer_date
FROM Customers AS c
JOIN orders AS o
ON c.customer_id = o.customer_id
WHERE o.order_delivered_customer_date > o.order_estimated_delivery_date;

-- 8. Identify top-selling products and the customers who purchased them
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       p.product_id, COUNT(p.product_id) AS product_sales
FROM Customers AS c
JOIN orders AS o
ON c.customer_id = o.customer_id
JOIN OrderItems AS oi
ON o.order_id = oi.order_id
JOIN ProductsData AS p
ON oi.product_id = p.product_id
GROUP BY c.customer_id, c.customer_first_name, c.customer_last_name, 
         p.product_id
ORDER BY product_sales DESC;

-- 9. Retrieve the most frequently purchased product categories by customers
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       p.product_category_name, COUNT(oi.product_id) AS total_purchases
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
JOIN OrderItems AS oi
ON o.order_id = oi.order_id
JOIN ProductsData AS p
ON oi.product_id = p.product_id
GROUP BY c.customer_id, c.customer_first_name, c.customer_last_name, 
         p.product_category_name
ORDER BY total_purchases DESC;

-- 10. Find customers who haven’t placed any orders
SELECT c.customer_id, c.customer_first_name, c.customer_last_name
FROM Customers AS c
LEFT JOIN orders AS o
ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- 11. Calculate average order delivery time for each customer
-- WRONGGG -> NEED FIX
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       AVG(DATEDIFF(DAY,o.order_delivered_customer_date, o.order_purchase_timestamp)) AS avg_delivery_time
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
WHERE o.order_delivered_customer_date IS NOT NULL and o.order_purchase_timestamp is not null
GROUP BY c.customer_id, c.customer_first_name, c.customer_last_name
ORDER BY avg_delivery_time DESC;

-- 12. Get top 5 customers with the highest total payments
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       SUM(p.payment_value) AS total_payment
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
JOIN OrderPayments AS p
ON o.order_id = p.order_id
GROUP BY c.customer_id, c.customer_first_name, c.customer_last_name
ORDER BY total_payment DESC;

-- 13. Identify customers who placed orders but haven’t reviewed any products
SELECT c.customer_id, c.customer_first_name, c.customer_last_name
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
LEFT JOIN OrderReviews AS r
ON o.order_id = r.order_id
WHERE r.review_id IS NULL;

-- 15. Update customer email address
UPDATE Customers
SET customer_email = 'newemail@example.com'
WHERE customer_id = '06b8999e2fba1a1fbc88172c00ba8bc7';

-- 16. Find the most popular payment types
SELECT p.payment_type, COUNT(p.payment_type) AS payment_count
FROM OrderPayments AS p
GROUP BY p.payment_type
ORDER BY payment_count DESC;

-- 17. Identify customers with the highest average review score
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       AVG(r.review_score) AS avg_review_score
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
JOIN OrderReviews AS r
ON o.order_id = r.order_id
GROUP BY c.customer_id, c.customer_first_name, c.customer_last_name
ORDER BY avg_review_score DESC;

-- 18. List products with the highest shipping fees and the customers who ordered them
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       p.product_id, p.product_category_name, oi.freight_value
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
JOIN OrderItems AS oi
ON o.order_id = oi.order_id
JOIN ProductsData AS p
ON oi.product_id = p.product_id
ORDER BY oi.freight_value DESC;

-- 19. Find customers who paid more in shipping than for the product itself
SELECT c.customer_id, c.customer_first_name, c.customer_last_name, 
       oi.product_id, oi.price, oi.freight_value
FROM Customers AS c
JOIN Orders AS o
ON c.customer_id = o.customer_id
JOIN OrderItems AS oi
ON o.order_id = oi.order_id
WHERE oi.freight_value > oi.price;

-- 20. Determine the total number of customers by state
SELECT customer_state, COUNT(customer_id) AS total_customers
FROM Customers
GROUP BY customer_state
ORDER BY total_customers DESC;

