# Vestiq - fashion search app. Reads only local files, so it works without the Hadoop cluster.
import re
from pathlib import Path
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent
RES = BASE.parent / "docs" / "results"
st.set_page_config(page_title="Vestiq", page_icon="👗", layout="wide")

GENDERS = {"men": "men", "man": "men", "mens": "men", "women": "women", "woman": "women", "womens": "women",
           "ladies": "women", "girl": "girls", "girls": "girls", "boy": "boys", "boys": "boys",
           "kid": "kids", "kids": "kids"}
ALLOWED = {"men": ["men", "unisex"], "women": ["women", "unisex"], "boys": ["boys", "kids", "unisex"],
           "girls": ["girls", "kids", "unisex"], "kids": ["kids", "boys", "girls", "unisex"]}
# Hand-made synonym and occasion map (a limitation: it is not learned from data).
ALIASES = {"kurti": ["kurta", "kurtas"], "tshirt": ["t shirt", "tshirts"], "tee": ["t shirt"],
           "sari": ["saree"], "jean": ["jeans"], "trouser": ["trousers"],
           "wedding": ["festive", "ethnic", "embroidered", "silk", "zari"],
           "traditional": ["ethnic", "embroidered", "woven", "silk"],
           "party": ["sequin", "embellished", "satin", "bodycon"],
           "birthday": ["party", "dress", "printed"],
           "college": ["casual", "printed", "cotton"], "office": ["formal", "solid", "slim"],
           "summer": ["cotton", "linen", "floral", "pastel"], "casual": ["printed", "cotton"],
           "corset": ["tie up", "lace up", "drawstring"]}
STOP = set("the for and with show find want need some please outfit outfits wear looking something that".split())

@st.cache_data
def load_catalog():
    df = pd.read_csv(BASE / "data" / "app_catalog.csv.gz")
    df["category"] = df["category"].fillna("").astype(str)
    df["text"] = (df["name"].fillna("") + " " + df["slug_text"].fillna("") + " " + df["category"]).str.lower()
    q = df["quality_score"]
    df["q_norm"] = (q - q.min()) / (q.max() - q.min())
    return df

def parse(query):
    q = query.lower()
    m = re.search(r"(?:under|below|less than|within|upto|up to|max|maximum|<)\s*(?:rs\.?|₹|inr)?\s*(\d[\d,]*)", q)
    budget = float(m.group(1).replace(",", "")) if m else None
    if m:
        q = q.replace(m.group(0), " ")
    tokens = re.findall(r"[a-z]+", q)
    gender = next((GENDERS[t] for t in tokens if t in GENDERS), None)
    terms = [t for t in tokens if t not in STOP and t not in GENDERS and len(t) > 2]
    return budget, gender, terms

def variants(t):
    v = {t, t + "s"}
    if t.endswith("s"):
        v.add(t[:-1])
    v.update(ALIASES.get(t, []))
    return v

def search(df, query, topn):
    budget, gender, terms = parse(query)
    d = df
    if budget:
        d = d[d["price"] <= budget]
    if gender:
        d = d[d["gender"].isin(ALLOWED[gender])]
    if terms:
        hits = pd.DataFrame({t: d["text"].str.contains("|".join(re.escape(x) for x in variants(t)), regex=True)
                             for t in terms})
        d = d.assign(text_score=hits.mean(axis=1))
        d = d[d["text_score"] > 0]
    else:
        d = d.assign(text_score=0.0)
    # Ranking: 55% text match + 30% quality (adjusted rating + popularity) + 15% discount
    d = d.assign(score=(0.55 * d["text_score"] + 0.30 * d["q_norm"]
                        + 0.15 * d["discount_pct"].clip(0, 100) / 100).round(3))
    return budget, gender, terms, d.sort_values("score", ascending=False).head(topn)

def read_table(name, **kw):
    p = RES / name
    return pd.read_csv(p, **kw) if p.exists() else None

st.title("👗 Vestiq: fashion search on a Hadoop + Spark pipeline")
tab_search, tab_insights, tab_about = st.tabs(["Search", "Insights", "About"])

with tab_search:
    df = load_catalog()
    query = st.text_input("What are you looking for?", placeholder="cute party dress under 3000")
    topn = st.slider("Results", 5, 50, 15)
    if query:
        budget, gender, terms, res = search(df, query, topn)
        st.caption(f"Understood: budget {'up to ₹%d' % budget if budget else 'any'}, "
                   f"for {gender or 'anyone'}, keywords {terms}")
        if res.empty:
            st.warning("No matching products. Try fewer words or a higher budget.")
        else:
            st.dataframe(res[["name", "seller", "category", "price", "mrp", "discount_pct", "rating",
                              "rating_total", "score", "purl"]], use_container_width=True, hide_index=True,
                         column_config={"purl": st.column_config.LinkColumn("Myntra link")})
    st.caption(f"Catalogue: {len(df):,} highest-quality products out of about 1.06 million processed with Spark.")

with tab_insights:
    cat = read_table("pig_category_stats.txt", sep="\t", header=None,
                     names=["category", "products", "avg_price", "avg_discount", "avg_rating"])
    brand = read_table("pig_brand_stats.txt", sep="\t", header=None,
                       names=["seller", "products", "avg_price", "avg_discount", "avg_rating", "total_ratings"])
    seg = read_table("segments.txt")
    voc = read_table("vocab.txt", sep="\t", header=None, names=["word", "count"])
    if cat is not None:
        st.subheader("Categories (Pig on YARN)")
        st.bar_chart(cat.head(15).set_index("category")["products"])
        st.dataframe(cat.head(15), hide_index=True, use_container_width=True)
    if brand is not None:
        st.subheader("Top brands by total ratings (Pig on YARN)")
        st.dataframe(brand.head(15), hide_index=True, use_container_width=True)
    if seg is not None:
        st.subheader("Product segments (Spark MLlib KMeans)")
        st.dataframe(seg, hide_index=True, use_container_width=True)
    if voc is not None:
        st.subheader("Fashion vocabulary (MapReduce word count)")
        st.bar_chart(voc.sort_values("count", ascending=False).head(40).set_index("word")["count"])

with tab_about:
    st.markdown("""
**Pipeline:** Myntra CSV (1.3 GB) in **HDFS** → **Spark** cleaning on YARN (multi-line CSV, 1.06 M rows) →
**MapReduce** vocabulary → **Pig** brand/category analytics → **Hive** table and queries →
**Spark SQL / MLlib** quality scores and KMeans segments → this app.

**Cluster:** 1 master (NameNode, ResourceManager) + 2 workers (DataNode, NodeManager), HDFS replication 2.

**Limits:** data is a May 2023 snapshot; keyword and occasion synonyms are hand-made; the app searches the 100,000
highest-quality products; the cluster's inter-node network was slow, so heavy queries run in Spark SQL.
""")
