-- Vestiq: Hive queries that run without launching a MapReduce job (Hive's fetch task reads HDFS directly).
SET hive.fetch.task.conversion=more;
USE vestiq;

-- Q1: the table definition (schema over the cleaned data in HDFS)
DESCRIBE products;

-- Q2: first rows of the catalogue
SELECT id, name, seller, category, gender, price, mrp, discount_pct, rating FROM products LIMIT 10;

-- Q3: highly rated, cheap T-shirts
SELECT name, seller, price, discount_pct, rating, rating_total FROM products
WHERE category = 'tshirts' AND price < 500 AND rating >= 4.5 LIMIT 10;

-- Q4: heavily discounted, well reviewed products
SELECT name, seller, price, mrp, discount_pct, rating_total FROM products
WHERE discount_pct >= 70 AND rating >= 4.3 AND rating_total >= 1000 LIMIT 10;
