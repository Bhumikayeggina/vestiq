#!/bin/bash
# Checks everything that does not need the cluster: script syntax, the data file and the app itself.
cd /home/hadoop/vestiq || exit 1
fail=0
for f in $(find . -name '*.sh' -not -path './.git/*'); do
  bash -n "$f" || { echo "[FAIL] syntax error in $f"; fail=1; }
done
for f in $(find . -name '*.py' -not -path './.git/*'); do
  python3 -m py_compile "$f" || { echo "[FAIL] python error in $f"; fail=1; }
done
find . -name __pycache__ -prune -exec rm -rf {} +
gzip -t app/data/app_catalog.csv.gz && echo "[ OK ] catalogue file readable" || fail=1
python3 tests/test_app.py || fail=1
if [ $fail -eq 0 ]; then echo "ALL OFFLINE CHECKS PASSED"; else echo "SOME CHECKS FAILED"; fi
