#!/usr/bin/env python3
# Wrong greedy: batches trips starting from the NEAREST books instead of the
# farthest. Correct when K = 1 (every trip is a single book), wrong otherwise
# whenever a side's book count is not divisible by K.
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
for side in (pos, neg):
    for i in range(k - 1, len(side), k):
        ans += 2 * side[i]
    if len(side) % k:
        ans += 2 * side[-1]
best = 0
if pos:
    best = max(best, pos[-1])
if neg:
    best = max(best, neg[-1])
print(ans - best)
