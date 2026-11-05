-- Vestiq: Pig analytics on the cleaned Myntra catalogue (runs as MapReduce jobs on YARN).
data = LOAD '/vestiq/curated/myntra_clean' USING PigStorage('\t')
       AS (id:long, name:chararray, seller:chararray, category:chararray, gender:chararray,
           price:double, mrp:double, discount_pct:double, rating:double, rating_total:long,
           slug_text:chararray, purl:chararray);

good = FILTER data BY seller IS NOT NULL AND seller != '' AND price IS NOT NULL;

-- Statistics per brand (only brands with at least 50 products)
by_brand = GROUP good BY seller;
brand_stats = FOREACH by_brand GENERATE group AS seller, COUNT(good) AS products,
              ROUND(AVG(good.price)) AS avg_price, ROUND_TO(AVG(good.discount_pct), 1) AS avg_discount,
              ROUND_TO(AVG(good.rating), 2) AS avg_rating, SUM(good.rating_total) AS total_ratings;
big_brands = FILTER brand_stats BY products >= 50;
ranked_brands = ORDER big_brands BY total_ratings DESC;
top_brands = LIMIT ranked_brands 100;
STORE top_brands INTO '/vestiq/staging/pig_brand_stats' USING PigStorage('\t');

-- Statistics per category
by_cat = GROUP good BY category;
cat_stats = FOREACH by_cat GENERATE group AS category, COUNT(good) AS products,
            ROUND(AVG(good.price)) AS avg_price, ROUND_TO(AVG(good.discount_pct), 1) AS avg_discount,
            ROUND_TO(AVG(good.rating), 2) AS avg_rating;
ranked_cats = ORDER cat_stats BY products DESC;
STORE ranked_cats INTO '/vestiq/staging/pig_category_stats' USING PigStorage('\t');
