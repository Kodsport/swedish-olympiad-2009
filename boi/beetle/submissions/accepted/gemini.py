t = []
while len(t) < 2:
    t += input().split()
n = int(t[0])
m = int(t[1])
while len(t) < n + 2:
    t += input().split()
x = [int(i) for i in t[2:n+2]]

z = 0 in x
if not z:
    x.append(0)
x.sort()
s = x.index(0)
v = len(x)

ans = m if z else 0
inf = 10**15

for k in range(1, n + 1):
    d0 = [inf] * v
    d1 = [inf] * v
    d0[s] = 0
    d1[s] = 0
    p = inf
    
    mx_l = min(k + (0 if z else 1) + 1, v)
    
    for l in range(1, mx_l + 1):
        nd0 = [inf] * v
        nd1 = [inf] * v
        for i in range(max(0, s - l + 1), min(s + 1, v - l + 1)):
            j = i + l - 1
            r = l if z else l - 1
            v0 = d0[i]
            v1 = d1[i]
            
            if v0 == inf and v1 == inf:
                continue
                
            if r == k:
                if v0 < p: p = v0
                if v1 < p: p = v1
                continue
                
            rem = k - r
            
            if v0 != inf:
                if i > 0:
                    c = v0 + (x[i] - x[i-1]) * rem
                    if c < nd0[i-1]: nd0[i-1] = c
                if j + 1 < v:
                    c = v0 + (x[j+1] - x[i]) * rem
                    if c < nd1[i]: nd1[i] = c
                    
            if v1 != inf:
                if i > 0:
                    c = v1 + (x[j] - x[i-1]) * rem
                    if c < nd0[i-1]: nd0[i-1] = c
                if j + 1 < v:
                    c = v1 + (x[j+1] - x[j]) * rem
                    if c < nd1[i]: nd1[i] = c
        d0 = nd0
        d1 = nd1
        
    if p != inf:
        cur = k * m - p
        if cur > ans:
            ans = cur
            
print(ans)
