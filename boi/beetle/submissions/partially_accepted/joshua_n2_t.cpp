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

ll test(vector<vector<vvi>>& dp, vi& water, ll leftMost, ll rightMost, bool left, ll t, ll m, ll score)
{
    if (t >= m)
    {
        return score;
    }

    ll& v = dp[leftMost][rightMost][left][t];

    if (v != -1) return v+score;

    ll ret = score;

    ll pos = water[(left) ? leftMost : rightMost];

    ll index = leftMost;
    if (index - 1 >= 0)
    {
        ll arrivalT = t + abs(water[index - 1] - pos);
        ret = max(ret,test(dp, water, min(leftMost, index - 1), max(rightMost, index - 1), true, arrivalT, m, score+max(0LL, m-arrivalT)));
    }

    index = rightMost;
    if (index + 1 < water.size())
    {
        ll arrivalT = t + abs(water[index + 1] - pos);
        ret = max(ret,test(dp, water, min(leftMost, index + 1), max(rightMost, index + 1), false, arrivalT, m, score + max(0LL, m - arrivalT)));
    }

    return ret;
}

int main()
{
    cin.tie(0)->sync_with_stdio(0);

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

    vector<vector<vvi>> bounds(n, vector<vvi>(n, vvi(2, vi(m,- 1))));
    cout << test(bounds, water, index,index, false, 0, m, 0)+free;

    return 0;
}

