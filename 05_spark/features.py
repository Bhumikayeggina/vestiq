# Vestiq - Spark SQL / DataFrames: analytics, quality scoring and the catalogue for the app.
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("vestiq-features").getOrCreate()
schema = ("id LONG, name STRING, seller STRING, category STRING, gender STRING, price DOUBLE, "
          "mrp DOUBLE, discount_pct DOUBLE, rating DOUBLE, rating_total LONG, slug_text STRING, purl STRING")
df = spark.read.schema(schema).option("sep", "\t").csv("hdfs:///vestiq/curated/myntra_clean")
df.createOrReplaceTempView("products")
print("ROWS:", df.count())

# ---- Analytics (these replace the slow Hive aggregate queries) ----
print("TOP CATEGORIES")
spark.sql("""SELECT category, COUNT(*) AS products, ROUND(AVG(price)) AS avg_price,
             ROUND(AVG(discount_pct),1) AS avg_discount FROM products
             GROUP BY category ORDER BY products DESC LIMIT 15""").show(truncate=False)
print("GENDER SPLIT")
spark.sql("""SELECT gender, COUNT(*) AS products, ROUND(AVG(price)) AS avg_price
             FROM products GROUP BY gender ORDER BY products DESC""").show()
print("PRICE BANDS")
spark.sql("""SELECT CASE WHEN price<500 THEN '1. under 500' WHEN price<1000 THEN '2. 500-999'
             WHEN price<2000 THEN '3. 1000-1999' WHEN price<3000 THEN '4. 2000-2999' ELSE '5. 3000+' END AS band,
             COUNT(*) AS products, ROUND(AVG(rating),2) AS avg_rating FROM products
             GROUP BY 1 ORDER BY 1""").show()
print("TOP BRANDS")
spark.sql("""SELECT seller, COUNT(*) AS products, ROUND(AVG(price)) AS avg_price, ROUND(AVG(rating),2) AS avg_rating
             FROM products GROUP BY seller HAVING COUNT(*) >= 100 ORDER BY products DESC LIMIT 15""").show(truncate=False)

# ---- Quality score: Bayesian-adjusted rating + popularity ----
C = spark.sql("SELECT AVG(rating) FROM products WHERE rating > 0").first()[0]
M = 100.0
v = F.coalesce(F.col("rating_total"), F.lit(0)).cast("double")
r = F.coalesce(F.col("rating"), F.lit(0.0))
scored = (df.withColumn("bayes_rating", F.round((v/(v+M))*r + (M/(v+M))*F.lit(C), 3))
            .withColumn("popularity", F.log1p(v)))
maxpop = scored.agg(F.max("popularity")).first()[0]
scored = scored.withColumn("quality_score",
         F.round(0.6*F.col("bayes_rating")/5.0 + 0.4*F.col("popularity")/F.lit(maxpop), 4)).drop("popularity")

# ---- Catalogue for the app: the 100,000 highest-quality products ----
(scored.orderBy(F.col("quality_score").desc()).limit(100000)
       .coalesce(1).write.mode("overwrite").option("header", True)
       .csv("hdfs:///vestiq/output/app_catalog"))
spark.stop()
