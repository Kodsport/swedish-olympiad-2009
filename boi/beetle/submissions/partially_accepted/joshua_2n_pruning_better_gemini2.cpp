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

// Pareto frontier cache: [leftMost][rightMost][isLeft] -> vector of {time, score}
vector<pair<ll, ll>> memo[305][305][2];

void test(const vi& water, ll leftMost, ll rightMost, bool left, ll t, ll m, ll score)
{
    ans = max(ans, score);
    
    if (t >= m) return;

    // --- PRUNING 1: Pareto Dominance ---
    // If we've been to this exact interval, on this side, with a better/equal time 
    // AND a better/equal score, this branch is mathematically dead.
    auto& state_history = memo[leftMost][rightMost][left];
    for (const auto& past_state : state_history) {
        if (past_state.first <= t && past_state.second >= score) {
            return; // Dominated!
        }
    }
    
    // Filter out past states that our CURRENT path strictly dominates to keep the list tiny
    vector<pair<ll, ll>> new_history;
    for (const auto& past_state : state_history) {
        if (t <= past_state.first && score >= past_state.second) continue; 
        new_history.push_back(past_state);
    }
    new_history.push_back({t, score});
    state_history = new_history;

    ll pos = water[left ? leftMost : rightMost];

    // --- PRUNING 2: The "No-Cloning" Tighter Bound ---
    ll pure_left_score = 0;
    ll pure_right_score = 0;
    ll closest_left_dist = (leftMost > 0) ? abs(water[leftMost - 1] - pos) : inf;
    ll closest_right_dist = (rightMost + 1 < sz(water)) ? abs(water[rightMost + 1] - pos) : inf;

    // Calculate max water if we only went Left
    for (int i = 0; i < leftMost; ++i) {
        ll min_arrival = t + abs(water[i] - pos);
        if (min_arrival < m) pure_left_score += (m - min_arrival);
    }
    
    // Calculate max water if we only went Right
    for (int i = rightMost + 1; i < sz(water); ++i) {
        ll min_arrival = t + abs(water[i] - pos);
        if (min_arrival < m) pure_right_score += (m - min_arrival);
    }

    // Best absolute case: We either only go left, only go right, or we do a crossover.
    // If we crossover, the second side we visit is delayed by AT LEAST 2 * (distance to the first drop of the first side).
    ll crossover_delay = 2 * min(closest_left_dist, closest_right_dist);
    ll right_delayed_score = 0;
    ll left_delayed_score = 0;

    if (crossover_delay < inf) {
        for (int i = 0; i < leftMost; ++i) {
            ll min_arrival = t + crossover_delay + abs(water[i] - pos);
            if (min_arrival < m) left_delayed_score += (m - min_arrival);
        }
        for (int i = rightMost + 1; i < sz(water); ++i) {
            ll min_arrival = t + crossover_delay + abs(water[i] - pos);
            if (min_arrival < m) right_delayed_score += (m - min_arrival);
        }
    }

    ll optimistic_future_score = max({
        pure_left_score, 
        pure_right_score, 
        pure_left_score + right_delayed_score, 
        pure_right_score + left_delayed_score
    });

    if (score + optimistic_future_score <= ans) return;


    // --- DFS EXECUTIONS ---
    // Try going Left
    if (leftMost - 1 >= 0) {
        ll arrivalT = t + abs(water[leftMost - 1] - pos);
        if (arrivalT < m) {
            test(water, leftMost - 1, rightMost, true, arrivalT, m, score + (m - arrivalT));
        }
    }

    // Try going Right
    if (rightMost + 1 < sz(water)) {
        ll arrivalT = t + abs(water[rightMost + 1] - pos);
        if (arrivalT < m) {
            test(water, leftMost, rightMost + 1, false, arrivalT, m, score + (m - arrivalT));
        }
    }
}

int main()
{
    cin.tie(0)->sync_with_stdio(0);

    ll n, m;
    if (!(cin >> n >> m)) return 0;

    vector<ll> water(n);
    repe(v, water) cin >> v;
    
    ll free = 0;
    sort(all(water));

    auto it = lower_bound(all(water), 0);

    if (it == end(water) || *it != 0) {
        it = water.insert(it, 0);
    } else {
        free = m;
    }

    n = water.size();
    ll index = it - water.begin();

    test(water, index, index, false, 0, m, 0);
    cout << ans + free << "\n";

    return 0;
}