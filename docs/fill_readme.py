# Fills the "Key results" section of README.md from the saved result files (run once after the Spark jobs).
import re
from pathlib import Path

root = Path("/home/hadoop/vestiq")

def read(p):
    f = root / p
    return f.read_text(errors="ignore") if f.exists() else ""

sql, ml = read("docs/spark_sql_results.txt"), read("docs/spark_ml_results.txt")
cats = [l.split("\t") for l in read("docs/results/pig_category_stats.txt").splitlines() if l.strip()]
seg = [l for l in read("docs/results/segments.txt").splitlines() if l.strip()]
vocab = [l.split("\t") for l in read("docs/results/vocab.txt").splitlines() if "\t" in l]

lines = []
m = re.search(r"ROWS:\s*(\d+)", sql)
if m:
    lines.append(f"- **{int(m.group(1)):,}** cleaned products processed with Spark SQL on YARN")
if cats:
    lines.append(f"- Largest category: **{cats[0][0]}** ({int(cats[0][1]):,} products, average price Rs {cats[0][2]})")
    lines.append(f"- **{len(cats)}** product categories analysed with Pig")
m = re.search(r"SILHOUETTE SCORE:\s*(-?[\d.]+)", ml)
if m:
    lines.append(f"- KMeans segmentation: **{max(len(seg) - 1, 0)} segments**, silhouette score **{float(m.group(1)):.2f}**")
if vocab:
    top = sorted(vocab, key=lambda r: -int(r[1]))[:8]
    lines.append("- Most frequent description words (MapReduce): " + ", ".join(w for w, _ in top))

readme = root / "README.md"
text = readme.read_text()
block = "\n".join(lines) if lines else "TODO: add results"
text = re.sub(r"TODO: replace this line[^\n]*", block, text)
readme.write_text(text)
print(block)
