// Cheese probe: "double sweep" heuristic — Dijkstra from node 1, then
// Dijkstra from the farthest node found, output that eccentricity.
// Exact on trees, wrong on general graphs; the antisweep cases catch it.
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int n, m;
vector<vector<pair<int,int>>> adj;

vector<ll> dijkstra(int src) {
    vector<ll> dist(n + 1, LLONG_MAX);
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u])
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    return dist;
}

int main() {
    cin.tie()->sync_with_stdio(0);
    cin >> n >> m;
    adj.assign(n + 1, {});
    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        adj[a].push_back({b, w});
        adj[b].push_back({a, w});
    }
    vector<ll> d1 = dijkstra(1);
    int u = (int)(max_element(d1.begin() + 1, d1.end()) - d1.begin());
    vector<ll> d2 = dijkstra(u);
    int v = (int)(max_element(d2.begin() + 1, d2.end()) - d2.begin());
    cout << u << ' ' << v << ' ' << d2[v] * 100 << '\n';
    return 0;
}
