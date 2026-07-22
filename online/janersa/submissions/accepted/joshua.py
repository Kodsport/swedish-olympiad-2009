from heapq import heappop, heappush

n=int(input())
m=int(input())
adj=[[] for i in range(n)]
for i in range(m):
    a,b,w=map(int,input().split())
    a-=1
    b-=1
    adj[a].append((b,w))
    adj[b].append((a,w))


a=b=-1
longest=-1
for i in range(n):
    dist = [10**9] * n
    dist[i]=0
    pq = []
    heappush(pq, (0, i))
    while len(pq):
        d,u = heappop(pq)
        if d > dist[u]:
            continue

        for e,w in adj[u]:
            if d+w < dist[e]:
                dist[e]=d+w
                heappush(pq, (d+w,e))

    if max(dist) > longest:
        longest = max(dist)
        a=i
        b=dist.index(longest)

print(a+1,b+1,100*longest)
