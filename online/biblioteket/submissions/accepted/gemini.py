n, k = map(int, input().split())
p = []
q = []
for _ in range(n):
    x = int(input())
    if x > 0:
        p.append(x)
    elif x < 0:
        q.append(-x)
p.sort()
q.sort()
ans = 0
for i in range(len(p) - 1, -1, -k):
    ans += 2 * p[i]
for i in range(len(q) - 1, -1, -k):
    ans += 2 * q[i]
m = 0
if p:
    m = max(m, p[-1])
if q:
    m = max(m, q[-1])
ans -= m
print(ans)
