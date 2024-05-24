#!/usr/bin/python3
import re
import sys

int_pat = "(0|[1-9][0-9]*)"

line = sys.stdin.readline()
assert re.match("^" + int_pat + "$", line)
n = int(line)
assert 2 <= n <= 100

line = sys.stdin.readline()
assert re.match("^" + int_pat + "$", line)
v = int(line)
assert 2 <= v <= 500

for i in range(v):
    line = sys.stdin.readline()
    assert re.match("^" + int_pat + " " + int_pat + " " + int_pat + "$", line)
    a, b, l = [int(x) for x in line.split()]
    assert 1 <= a <= n
    assert 1 <= b <= n

line = sys.stdin.readline()
assert len(line) == 0

sys.exit(42)
