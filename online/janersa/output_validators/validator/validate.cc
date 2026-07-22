#include "validate.h"
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int n, m;
vector<vector<pair<int,int>>> adj;

ll dijkstra(int src, int dest) {
    vector<ll> dist(n, LLONG_MAX);
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;
        if (u==dest) return d;
        for (auto [v, w] : adj[u])
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    judge_error("Invalid input: more than one connected component");
}

int main(int argc, char **argv) {
    init_io(argc, argv);

    judge_in >> n >> m;
    adj.assign(n, {});
    for (int i = 0; i < m; i++) {
        int a, b, w;
        judge_in >> a >> b >> w;
        a--; b--;
        adj[a].push_back({b, w});
        adj[b].push_back({a, w});
    }

    auto check = [&](istream& sol, feedback_function feedback){
        int a,b,l;
        if(!(sol >> a >> b >> l)) feedback("Expected more output");
        if (a < 1 || a > n || b < 1 || b > n) feedback("a or b out of range");
        if (a == b) feedback("a == b not allowed");
        ll d = dijkstra(a-1, b-1);
        if (d*100!=l) feedback("Output length does not match dist(a,b)");

        string trailing;
        if(sol >> trailing) feedback("Trailing output");
        return l;
    };

    ll judge_length = check(judge_ans, judge_error);
    ll contestant_length = check(author_out, wrong_answer);

    if (judge_length < contestant_length)
        judge_error("NO! Contestant found better solution than judge");

    if (contestant_length < judge_length)
        wrong_answer("WA: contestant found suboptimal solution");

    accept();
}
