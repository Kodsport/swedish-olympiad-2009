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

using p3 = tuple<int,int,int>;
using vp3 = vector<p3>;
using vvp3 = vector<vp3>;
using vvvp3 = vector<vvp3>;
ll test(vvvp3& dp, vi& water, ll leftMost, ll rightMost, bool left, ll t, ll m, ll score)
{
    if (t >= m)
    {
        return score;
    }

    p3& v = dp[leftMost][rightMost][left];
    ll dpIncrease, dpT, dpScore;
    tie(dpIncrease, dpT, dpScore) = v;

    if (dpIncrease != -1 && dpT < t && dpScore >= score) return -inf;
    if (dpIncrease != -1 && dpT == t) return dpIncrease+score;

    ll ret = score;

    ll pos = water[(left) ? leftMost : rightMost];

    ll index = leftMost;
    if (index - 1 >= 0)
    {
        ll arrivalT = t + abs(water[index - 1] - pos);
        ret = max(ret, test(dp, water, min(leftMost, index - 1), max(rightMost, index - 1), true, arrivalT, m, score + max(0LL, m - arrivalT)));
    }

    index = rightMost;
    if (index + 1 < water.size())
    {
        ll arrivalT = t + abs(water[index + 1] - pos);
        ret = max(ret, test(dp, water, min(leftMost, index + 1), max(rightMost, index + 1), false, arrivalT, m, score + max(0LL, m - arrivalT)));
    }

    v = { ret - score,t, score };

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

    ll index;
    if (it == water.end())
    {
        water.emplace_back(0);
        index = water.size()-1;
    }
    else if (*it != 0)
    {
        it = water.insert(it, 0);
        index = it - water.begin();
    }
    else
    {
        free = m;
        index = it - water.begin();
    }

    n = water.size();

    vvvp3 bounds(n, vvp3(n, vp3(2, { -1,-1, -1 })));
    cout << test(bounds, water, index, index, false, 0, m, 0) + free;

    return 0;
}
