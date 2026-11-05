# Vestiq - Spark MLlib: KMeans segments products by price, discount, rating and popularity.
from pyspark.sql import SparkSession, functions as F
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator

spark = SparkSession.builder.appName("vestiq-ml").getOrCreate()
schema = ("id LONG, name STRING, seller STRING, category STRING, gender STRING, price DOUBLE, "
          "mrp DOUBLE, discount_pct DOUBLE, rating DOUBLE, rating_total LONG, slug_text STRING, purl STRING")
df = (spark.read.schema(schema).option("sep", "\t").csv("hdfs:///vestiq/curated/myntra_clean")
      .filter(F.col("price") > 0).na.fill({"rating": 0.0, "rating_total": 0, "discount_pct": 0.0}))

feat = (df.select("id", "price", "discount_pct", "rating", "rating_total")
        .withColumn("log_price", F.log1p("price")).withColumn("log_votes", F.log1p("rating_total")))
vec = VectorAssembler(inputCols=["log_price", "discount_pct", "rating", "log_votes"], outputCol="raw").transform(feat)
data = (StandardScaler(inputCol="raw", outputCol="features", withMean=True, withStd=True)
        .fit(vec).transform(vec).cache())

model = KMeans(k=6, seed=42, maxIter=20, featuresCol="features").fit(data)
pred = model.transform(data)
sil = ClusteringEvaluator(featuresCol="features", metricName="silhouette").evaluate(pred.sample(False, 0.05, 42))
print("SILHOUETTE SCORE:", sil)

prof = (pred.groupBy("prediction").agg(
        F.count("*").alias("products"), F.round(F.avg("price")).alias("avg_price"),
        F.round(F.avg("discount_pct"), 1).alias("avg_discount"),
        F.round(F.avg(F.when(F.col("rating") > 0, F.col("rating"))), 2).alias("avg_rating"),
        F.round(F.avg("rating_total")).alias("avg_votes")).orderBy("prediction"))
prof.show()
prof.coalesce(1).write.mode("overwrite").option("header", True).csv("hdfs:///vestiq/output/segments")
spark.stop()
