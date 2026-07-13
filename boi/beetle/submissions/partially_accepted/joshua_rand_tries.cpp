#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using vi = vector<ll>;
using vvi = vector<vi>;
using p2 = pair<ll,ll>;
const ll inf = 1e18;

#define repe(i, arr) for (auto& i : arr)
#define rep(i, b) for(ll i = 0; i < (b); ++i)
#define repp(i, a, b) for(ll i = a; i < (b); ++i)
#define all(x) begin(x),end(x)
#define sz(x) ((ll)x.size())

int main()
{
    cin.tie(0)->sync_with_stdio(0);
    auto start = chrono::high_resolution_clock::now();

    ll n, m;
    cin >> n >> m;

    vector<ll> water(n);
    repe(v, water) cin >> v;

    ll free = 0;

    sort(all(water));

    auto it = lower_bound(all(water), 0);

    if (it == end(water) || *it != 0)
    {
        it = water.insert(it, 0);
    }
    else
    {
        free = m;
    }

    n = water.size();
    ll index = it - water.begin();

    mt19937 rng(42);
    uniform_int_distribution<int> dist(0,1);
    ll ans = 0;
    while (true) {
        int dur = chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now() - start).count();
        if (dur > 950) break;

        ll leftmost = index, rightmost = index;
        bool left = true;
        ll t = 0;

        ll tot_water = 0;
        while (leftmost > 0 && rightmost < n - 1 && t < m) {
            int pos = water[left ? leftmost : rightmost];
            if (dist(rng) % 2) {
                leftmost--;
                left = true;
                t += abs(pos-water[leftmost]);
            }
            else {
                rightmost++;
                left = false;
                t += abs(pos-water[rightmost]);
            }
            tot_water += max(0LL, m-t);
        }

        while (leftmost > 0 && t < m) {
            int pos = water[left ? leftmost : rightmost];
            leftmost--;
            left = true;
            t += abs(pos-water[leftmost]);
            tot_water += max(0LL, m-t);
        }

        while (rightmost < n - 1 && t < m) {
            int pos = water[left ? leftmost : rightmost];
            rightmost++;
            left = false;
            t += abs(pos-water[rightmost]);
            tot_water += max(0LL, m-t);
        }
        ans = max(ans, tot_water);
    }

    cout << ans+free << '\n';

    return 0;
}

