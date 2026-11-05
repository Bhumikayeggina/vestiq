#!/usr/bin/env python3
# MapReduce reducer (also used as combiner): sums the counts for each word.
import sys

current, total = None, 0
for line in sys.stdin:
    word, count = line.rstrip("\n").split("\t")
    if word == current:
        total += int(count)
    else:
        if current is not None:
            print(current + "\t" + str(total))
        current, total = word, int(count)
if current is not None:
    print(current + "\t" + str(total))
