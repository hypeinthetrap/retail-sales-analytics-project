SELECT product_category,
       SUM(total_amount) AS total_revenue
FROM transactions
GROUP BY product_category
ORDER BY total_revenue DESC;
