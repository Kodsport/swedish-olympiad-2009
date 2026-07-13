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

ll test(vector<vvi>& dp, vi& water, ll leftMost, ll rightMost, bool left, ll t, ll m, ll score)
{
    if ((leftMost == 0 && rightMost == water.size()-1) || t >= m)
    {
        return score;
    }

    ll& v = dp[leftMost][rightMost][left];

    if (v != -1) return v;

    ll index = leftMost;
    if (index > 0)
    {
        ll arrivalT = t + abs(water[index - 1] - water[(left)?leftMost:rightMost]);
        v = max(v,test(dp, water, min(leftMost, index - 1), max(rightMost, index - 1), true,  arrivalT, m, score+max(0LL, m-arrivalT)));
    }
    index = rightMost;
    if (index < water.size()-1)
    {
        ll arrivalT = t + abs(water[index + 1] - water[(left) ? leftMost : rightMost]);
        v = max(v,test(dp, water, min(leftMost, index + 1), max(rightMost, index + 1), false, arrivalT, m, score + max(0LL, m - arrivalT)));
    }

    return v;
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

    if (*it != 0)
    {
        it = water.insert(it, 0);
    }

    n = water.size();
    ll index = it - water.begin();

    vector<vvi> bounds(n, vvi(n, vi(2,- 1)));
    cout << test(bounds, water, index,index, false, 0, m, 0);

    return 0;
}

