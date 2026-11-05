# Vestiq - clean the raw Myntra catalogue with Spark on YARN.
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("vestiq-clean").getOrCreate()

# Read raw data from HDFS. multiLine=True because the image field spans several lines.
raw = (spark.read.option("header", True).option("multiLine", True)
       .option("quote", '"').option("escape", '"')
       .csv("hdfs:///vestiq/raw/myntra202305041052.csv"))

def txt(c):
    return F.trim(F.regexp_replace(F.regexp_replace(F.col(c), r'[\t\r\n"]+', ' '), r'\s+', ' '))

# Keep valid rows, cast types, drop the huge img column and the empty asin column.
df = (raw.filter(F.col("id").rlike("^[0-9]+$"))
      .select(F.col("id").cast("long").alias("id"),
              txt("name").alias("name"),
              txt("seller").alias("seller"),
              F.col("price").cast("double").alias("price"),
              F.col("mrp").cast("double").alias("mrp"),
              F.col("rating").cast("double").alias("rating"),
              F.col("ratingTotal").cast("long").alias("rating_total"),
              F.regexp_replace(F.col("purl"), r'[\s"]+', '').alias("purl")))

# Remove invalid prices; derive discount, category and description text from the product link.
parts = F.split(F.col("purl"), "/")
df = (df.filter((F.col("price") > 0) & (F.col("mrp") > 0))
      .withColumn("discount_pct", F.round((F.col("mrp") - F.col("price")) / F.col("mrp") * 100, 1))
      .withColumn("category", F.lower(parts.getItem(3)))
      .withColumn("slug_text", F.regexp_replace(parts.getItem(5), "-", " ")))

# Work out the gender from the name, or else from the link.
pat = r"\b(men|women|boys|girls|kids|unisex)\b"
g_name = F.regexp_extract(F.lower(F.col("name")), pat, 1)
g_slug = F.regexp_extract(F.col("slug_text"), pat, 1)
df = df.withColumn("gender", F.when(g_name != "", g_name).when(g_slug != "", g_slug).otherwise("unknown"))

out = df.select("id", "name", "seller", "category", "gender", "price", "mrp",
                "discount_pct", "rating", "rating_total", "slug_text", "purl")

# Write the cleaned data back to HDFS: tab separated, one row per line.
(out.coalesce(1).write.mode("overwrite").option("sep", "\t").option("header", False)
    .csv("hdfs:///vestiq/curated/myntra_clean"))
spark.stop()
