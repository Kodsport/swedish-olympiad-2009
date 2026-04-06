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

ll ans = 0;
void test(vi& water, ll leftMost, ll rightMost, bool left, ll t, ll m, ll score)
{
    ans = max(ans, score);
    
    // If time exceeds m, all remaining drops globally are empty
    if (t >= m) return;

    ll pos = water[left ? leftMost : rightMost];

    // --- PRUNING 1: The Straight-Line Distance Bound ---
    ll optimistic_future_score = 0;
    
    // Calculate max possible water from remaining left drops
    for (int i = 0; i < leftMost; ++i) {
        ll min_arrival = t + abs(water[i] - pos);
        if (min_arrival < m) {
            optimistic_future_score += (m - min_arrival);
        }
    }
    
    // Calculate max possible water from remaining right drops
    for (int i = rightMost + 1; i < sz(water); ++i) {
        ll min_arrival = t + abs(water[i] - pos);
        if (min_arrival < m) {
            optimistic_future_score += (m - min_arrival);
        }
    }

    // If our current score + absolute best-case future can't beat the max, kill the branch
    if (score + optimistic_future_score <= ans) return;


    // --- PRUNING 2: Evaporation Dead-Ends & Recursion ---
    
    // Try going Left
    if (leftMost - 1 >= 0) {
        ll arrivalT = t + abs(water[leftMost - 1] - pos);
        // Only branch if the adjacent drop actually has water. 
        // If it's dry, all drops further left are also definitively dry.
        if (arrivalT < m) {
            test(water, leftMost - 1, rightMost, true, arrivalT, m, score + (m - arrivalT));
        }
    }

    // Try going Right
    if (rightMost + 1 < sz(water)) {
        ll arrivalT = t + abs(water[rightMost + 1] - pos);
        // Same here: if the nearest right drop is dry, don't bother going right at all.
        if (arrivalT < m) {
            test(water, leftMost, rightMost + 1, false, arrivalT, m, score + (m - arrivalT));
        }
    }
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

    test(water, index,index, false, 0, m, 0);
    cout << ans+free;

    return 0;
}

