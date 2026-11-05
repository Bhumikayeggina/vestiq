SET hive.execution.engine=mr;
USE vestiq;

-- Q1: size and overall averages
SELECT COUNT(*) AS products, COUNT(DISTINCT seller) AS brands, COUNT(DISTINCT category) AS categories,
       ROUND(AVG(price)) AS avg_price, ROUND(AVG(discount_pct),1) AS avg_discount, ROUND(AVG(rating),2) AS avg_rating
FROM products;

-- Q2: top 15 categories by number of products
SELECT category, COUNT(*) AS products, ROUND(AVG(price)) AS avg_price, ROUND(AVG(discount_pct),1) AS avg_discount
FROM products GROUP BY category ORDER BY products DESC LIMIT 15;

-- Q3: split by gender
SELECT gender, COUNT(*) AS products, ROUND(AVG(price)) AS avg_price, ROUND(AVG(rating),2) AS avg_rating
FROM products GROUP BY gender ORDER BY products DESC;

-- Q4: price bands
SELECT CASE WHEN price < 500 THEN '1. under 500' WHEN price < 1000 THEN '2. 500-999'
            WHEN price < 2000 THEN '3. 1000-1999' WHEN price < 3000 THEN '4. 2000-2999'
            ELSE '5. 3000 and above' END AS price_band,
       COUNT(*) AS products, ROUND(AVG(rating),2) AS avg_rating
FROM products GROUP BY CASE WHEN price < 500 THEN '1. under 500' WHEN price < 1000 THEN '2. 500-999'
            WHEN price < 2000 THEN '3. 1000-1999' WHEN price < 3000 THEN '4. 2000-2999'
            ELSE '5. 3000 and above' END
ORDER BY price_band;

-- Q5: top 15 brands by number of products
SELECT seller, COUNT(*) AS products, ROUND(AVG(price)) AS avg_price, ROUND(AVG(rating),2) AS avg_rating
FROM products GROUP BY seller HAVING COUNT(*) >= 100 ORDER BY products DESC LIMIT 15;

-- Q6: discount bands
SELECT CASE WHEN discount_pct < 20 THEN '1. under 20%' WHEN discount_pct < 40 THEN '2. 20-39%'
            WHEN discount_pct < 60 THEN '3. 40-59%' ELSE '4. 60% and above' END AS discount_band,
       COUNT(*) AS products
FROM products GROUP BY CASE WHEN discount_pct < 20 THEN '1. under 20%' WHEN discount_pct < 40 THEN '2. 20-39%'
            WHEN discount_pct < 60 THEN '3. 40-59%' ELSE '4. 60% and above' END
ORDER BY discount_band;

-- Q7: best rated brands (at least 200 products)
SELECT seller, COUNT(*) AS products, ROUND(AVG(rating),2) AS avg_rating, SUM(rating_total) AS total_ratings
FROM products WHERE rating > 0 GROUP BY seller HAVING COUNT(*) >= 200 ORDER BY avg_rating DESC LIMIT 15;

-- Q8: biggest category and gender combinations
SELECT category, gender, COUNT(*) AS products, ROUND(AVG(discount_pct),1) AS avg_discount
FROM products GROUP BY category, gender HAVING COUNT(*) >= 5000 ORDER BY products DESC LIMIT 20;

-- Q9: most reviewed products
SELECT id, name, seller, price, rating, rating_total
FROM products ORDER BY rating_total DESC LIMIT 10;

-- Q10: how many products have a rating at all, per price band
SELECT CASE WHEN price < 1000 THEN 'under 1000' ELSE '1000 and above' END AS band,
       SUM(CASE WHEN rating > 0 THEN 1 ELSE 0 END) AS rated, COUNT(*) AS total
FROM products GROUP BY CASE WHEN price < 1000 THEN 'under 1000' ELSE '1000 and above' END;
