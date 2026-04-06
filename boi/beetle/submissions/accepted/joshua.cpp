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

ll n, m;

ll best(vector<vector<p2>>& dp, vi& drops, ll left, ll right, ll taken, bool leftSide, ll target, ll penalty)
{
    if (taken == target) return penalty;

    ll& v = leftSide ? dp[left][right].first : dp[left][right].second;
    if (v != -1) return v + penalty;

    ll ret = inf;

    ll pos = drops[(leftSide) ? left : right];

    if (left - 1 >= 0)
    {
        ret = min(ret, best(dp, drops, left - 1, right, taken + 1, true, target, penalty + (target - taken) * abs(drops[left - 1] - pos)));
    }

    if (right + 1 < sz(drops))
    {
        ret = min(ret, best(dp, drops, left, right + 1, taken + 1, false, target, penalty + (target - taken) * abs(drops[right + 1] - pos)));
    }

    v = ret - penalty;

    return ret;
}


int main()
{
    cin.tie(0)->sync_with_stdio(0);

    cin >> n >> m;

    vector<ll> drops(n);
    repe(v, drops) cin >> v;
    sort(all(drops));

    auto it = lower_bound(all(drops), 0);


    bool free = false;
    ll index;
    if (it == drops.end())
    {
        drops.emplace_back(0);
        index = drops.size() - 1;
    }
    else if (*it != 0)
    {
        it = drops.insert(it, 0);
        index = it - drops.begin();
    }
    else
    {
        free = true;
        index = it - drops.begin();
    }


    ll ans = 0;
    vector<vector<p2>> dp(drops.size(), vector<p2>(drops.size(), {-1,-1}));
    repp(i, 1, n + 1)
    {
        ll penalty = best(dp, drops, index, index, free, false, i, 0);

        rep(j, sz(drops))
        {
            rep(k, sz(drops))
            {
                dp[j][k].first = -1;
                dp[j][k].second = -1;
            }
        }

        ans = max(ans, i * m - penalty);
    }

    cout << ans << '\n';

    return 0;
}

