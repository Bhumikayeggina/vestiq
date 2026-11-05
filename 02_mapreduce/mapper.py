#!/usr/bin/env python3
# MapReduce mapper: reads cleaned product rows (tab separated) and emits "word<TAB>1"
# for every word in the product description (column 11, slug_text).
import sys, re

STOP = {"the", "and", "with", "for", "buy", "set", "pack", "pcs", "combo", "pure"}

for line in sys.stdin:
    f = line.rstrip("\n").split("\t")
    if len(f) < 12:
        continue
    for w in re.findall(r"[a-z]+", f[10].lower()):
        if len(w) > 2 and w not in STOP:
            print(w + "\t1")
