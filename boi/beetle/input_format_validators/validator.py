#!/usr/bin/python3
import re
import sys

int_pat = "(0|-?[1-9][0-9]*)"
input2 = "^" + int_pat + " " + int_pat + "$"
input1 = "^" + int_pat + "$"

line = sys.stdin.readline()
assert re.match(input2, line)
n, m = [int(x) for x in line.split()]
assert 0 <= n <= 300 and 1 <= m <= 1000000

unique = set()

for i in range(n):
	line = sys.stdin.readline()
	assert re.match(input1, line)
	x = int(line)
	assert -10000 <= x <= 10000
	unique.add(x)

assert len(unique) == n

line = sys.stdin.readline()
assert len(line) == 0
sys.exit(42)
