#!/usr/bin/env python3
N, K = [int(x) for x in input().split()]
s = 0
mx = 0
for k in range(N):
    p = abs(int(input()))
    s += p
    mx = max(mx, abs(p))
print(2 * s - mx)
