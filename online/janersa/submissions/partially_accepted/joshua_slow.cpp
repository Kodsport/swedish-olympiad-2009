#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using vi = vector<ll>;
using vvi = vector<vi>;
using p2 = pair<ll, ll>;
const ll inf = 1e18;

#define rep(i,n) for (ll i = 0; i < (n); i++)
#define repp(i,a,n) for (ll i = (a); i < (n); i++)
#define repe(i, arr) for (auto& i : arr)
#define all(x) begin(x),end(x)
#define sz(x) ((ll)(x).size())

int main() {
    cin.tie()->sync_with_stdio(0);

    int n,m;
    cin >> n >> m;

    vector<vector<pair<int,int>>> adj(n);

    rep(i,m) {
        int a,b,w;
        cin >> a >> b >> w;
        a--; b--;
        adj[a].emplace_back(b,w);
        adj[b].emplace_back(a,w);
    }

    vector<int> dist(n);
    auto dijkstra = [&](int a, int b) {
        fill(all(dist),1e9);
        priority_queue<pair<int,int>> pq;
        pq.emplace(0,a);
        dist[a]=0;

        while (sz(pq)) {
            auto [d,u] = pq.top();
            pq.pop();
            d=-d;
            if (d>dist[u]) continue;
            if (u==b) return d;

            for (auto [e,w] : adj[u]) {
                if (w+d < dist[e]) {
                    dist[e]=w+d;
                    pq.emplace(-(w+d), e);
                }
            }
        }
        assert(0);
    };

    int longest = -1;
    int a = -1;
    int b = -1;

    rep(i,n) {
        repp(j,i+1,n) {
            int d = dijkstra(i,j);
            if (d>longest) {
                a=i;
                b=j;
                longest=d;
            }
        }
    }

    cout << a+1 << ' ' << b+1 << ' ' << longest*100 << endl;

    return 0;
}
