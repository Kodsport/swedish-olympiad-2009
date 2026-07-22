#!/usr/bin/env python3
# Correct greedy, but assumes there are books on both sides of the origin.
# Crashes on single-sign inputs (the Python analogue of the out-of-bounds
# read in the original biblioteket.cpp).
n, k = map(int, input().split())
pos, neg = [], []
for _ in range(n):
    x = int(input())
    if x >= 0:
        pos.append(x)
    else:
        neg.append(-x)
pos.sort()
neg.sort()
ans = 0
for i in range(len(pos) - 1, -1, -k):
    ans += 2 * pos[i]
for i in range(len(neg) - 1, -1, -k):
    ans += 2 * neg[i]
ans -= max(pos[-1], neg[-1])
print(ans)
