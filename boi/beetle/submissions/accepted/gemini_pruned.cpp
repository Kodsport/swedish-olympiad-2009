#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const long long INF = 1e18;

void solve() {
    int n;
    long long m;
    if (!(cin >> n >> m)) return;
    
    vector<int> x(n);
    bool zero_is_drop = false;
    for (int i = 0; i < n; ++i) {
        cin >> x[i];
        if (x[i] == 0) zero_is_drop = true;
    }
    
    // Ensure the beetle's starting point (0) is in our points list
    vector<int> P = x;
    if (!zero_is_drop) {
        P.push_back(0);
    }
    sort(P.begin(), P.end());
    
    int total_points = P.size();
    int Z = 0;
    for (int i = 0; i < total_points; ++i) {
        if (P[i] == 0) {
            Z = i + 1; // 1-indexed position for DP
            break;
        }
    }
    
    vector<int> real_drops(total_points + 1, 0);
    for (int i = 0; i < total_points; ++i) {
        if (P[i] != 0 || zero_is_drop) {
            real_drops[i + 1] = 1;
        }
    }
    
    vector<int> prefix_real(total_points + 1, 0);
    for (int i = 1; i <= total_points; ++i) {
        prefix_real[i] = prefix_real[i - 1] + real_drops[i];
    }
    
    long long max_water = 0;
    int total_real = prefix_real[total_points];
    
    // Evaluate taking exactly K drops
    for (int K = 1; K <= total_real; ++K) {
        vector<vector<long long>> dp(total_points + 2, vector<long long>(2, INF));
        dp[Z][0] = 0;
        dp[Z][1] = 0;
        
        long long best_for_K = -1;
        
        // Edge case: Initial point happens to be a valid drop
        if (prefix_real[Z] - prefix_real[Z - 1] == K) {
            best_for_K = max(best_for_K, (long long)K * m);
        }
        
        // Expanding DP window size length `L`
        for (int L = 2; L <= total_points; ++L) {
            vector<vector<long long>> next_dp(total_points + 2, vector<long long>(2, INF));
            bool any_valid = false;
            
            for (int i = 1; i <= total_points - L + 1; ++i) {
                int j = i + L - 1;
                if (i > Z || j < Z) continue; // The interval MUST include the starting 0 position 
                
                int new_collected = prefix_real[j] - prefix_real[i - 1];
                if (new_collected > K) continue; // State becomes invalid if we forcefully collect > K 
                
                long long p_i = P[i - 1], p_j = P[j - 1];
                long long p_ip1 = P[i], p_jm1 = P[j - 2];
                
                // --- Transitions ending at the Left Bound (i) ---
                int old_col_0 = prefix_real[j] - prefix_real[i];
                long long R0 = K - old_col_0;
                
                if (dp[i + 1][0] != INF) {
                    next_dp[i][0] = min(next_dp[i][0], dp[i + 1][0] + (p_ip1 - p_i) * R0);
                }
                if (dp[i + 1][1] != INF) {
                    next_dp[i][0] = min(next_dp[i][0], dp[i + 1][1] + (p_j - p_i) * R0);
                }
                
                // --- Transitions ending at the Right Bound (j) ---
                int old_col_1 = prefix_real[j - 1] - prefix_real[i - 1];
                long long R1 = K - old_col_1;
                
                if (dp[i][0] != INF) {
                    next_dp[i][1] = min(next_dp[i][1], dp[i][0] + (p_j - p_i) * R1);
                }
                if (dp[i][1] != INF) {
                    next_dp[i][1] = min(next_dp[i][1], dp[i][1] + (p_j - p_jm1) * R1);
                }
                
                if (next_dp[i][0] != INF || next_dp[i][1] != INF) {
                    any_valid = true;
                }
                
                if (new_collected == K) {
                    long long pen = min(next_dp[i][0], next_dp[i][1]);
                    if (pen <= (long long)K * m) {
                        best_for_K = max(best_for_K, (long long)K * m - pen);
                    }
                }
            }
            if (!any_valid) break; // Pruning if no branches survive length constraints 
            dp = move(next_dp);
        }
        
        if (best_for_K != -1) {
            max_water = max(max_water, best_for_K);
        } else {
            // Prune Outer Loop: if we can't secure positive total water for K drops, we inherently won't for K+1
            break; 
        }
    }
    
    cout << max_water << "\n";
}

int main() {
    // Optimize standard I/O operations for speed
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    solve();
    return 0;
}
