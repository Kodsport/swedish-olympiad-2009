import sys

s = input().split()
if not s:
    exit()
n = int(s[0])
m = int(s[1])

if n == 0:
    print(0)
    exit()

x = []
for _ in range(n):
    x.append(int(input()))
x.sort()

l = [i for i in x if i < 0]
r = [i for i in x if i >= 0]

c = 0
t = 0
ans = 0
p = 0

while l or p < len(r):
    dl = abs(l[-1] - c) if l else 1e18
    dr = abs(r[p] - c) if p < len(r) else 1e18
    
    if dl < dr:
        tgt = l.pop()
        d = dl
    else:
        tgt = r[p]
        p += 1
        d = dr
    
    t += d
    v = m - t
    if v > 0:
        ans += v
        c = tgt
    else:
        break

print(ans)
