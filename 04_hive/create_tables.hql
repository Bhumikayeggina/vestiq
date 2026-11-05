-- Vestiq: Hive table over the cleaned Myntra data (tab-separated, written by the Spark job).
SET hive.execution.engine=mr;
CREATE DATABASE IF NOT EXISTS vestiq;
USE vestiq;
DROP TABLE IF EXISTS products;
CREATE EXTERNAL TABLE products (
  id BIGINT, name STRING, seller STRING, category STRING, gender STRING,
  price DOUBLE, mrp DOUBLE, discount_pct DOUBLE, rating DOUBLE,
  rating_total BIGINT, slug_text STRING, purl STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/vestiq/curated/myntra_clean';
