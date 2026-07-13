#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Structure to hold our Pareto front configurations
struct Point {
    int t; // time elapsed
    int w; // water collected
};

// DP State: dp[length_parity][left_index][pos]
// pos = 0 means we are at the left bound 'l'
// pos = 1 means we are at the right bound 'r'
vector<Point> dp[2][310][2];

// Merges two sorted Pareto fronts while calculating distances and dropping sub-optimal configurations
inline void merge_and_pareto(const vector<Point>& src1, int d1, int val, 
                             const vector<Point>& src2, int d2, 
                             vector<Point>& out, int& global_max) {
    int i = 0, j = 0;
    int n1 = src1.size(), n2 = src2.size();
    out.clear();
    
    int best_w = -1;

    // Two-pointer merge (since sources are already strictly increasing in time)
    while (i < n1 || j < n2) {
        int t_new, w_old;
        
        if (i < n1 && j < n2) {
            int t1 = src1[i].t + d1;
            int t2 = src2[j].t + d2;
            if (t1 < t2) {
                t_new = t1;
                w_old = src1[i].w;
                i++;
            } else if (t2 < t1) {
                t_new = t2;
                w_old = src2[j].w;
                j++;
            } else { // Times are equal, pick the configuration that had more water
                t_new = t1;
                w_old = max(src1[i].w, src2[j].w);
                i++;
                j++;
            }
        } else if (i < n1) {
            t_new = src1[i].t + d1;
            w_old = src1[i].w;
            i++;
        } else {
            t_new = src2[j].t + d2;
            w_old = src2[j].w;
            j++;
        }
        
        // Add water gained at the newly visited drop
        int w_new = w_old + (val > t_new ? val - t_new : 0);
        
        // If it strictly improves the maximum water for this specific time frame, keep it
        if (w_new > best_w) {
            out.push_back({t_new, w_new});
            best_w = w_new;
            if (w_new > global_max) {
                global_max = w_new;
            }
        }
    }
}

int main() {
    // Fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n, m_val;
    if (!(cin >> n >> m_val)) return 0;
    
    vector<int> X;
    X.reserve(n + 1);
    
    bool has_zero = false;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        X.push_back(x);
        if (x == 0) has_zero = true;
    }
    
    // Add artificial starting point if there isn't a drop at 0
    if (!has_zero) {
        X.push_back(0);
    }
    
    sort(X.begin(), X.end());
    
    int N = X.size();
    vector<int> M(N);
    int Z = -1;
    
    // Establish original quantities of water at each index
    for (int i = 0; i < N; i++) {
        if (X[i] == 0) {
            Z = i;
            M[i] = has_zero ? m_val : 0;
        } else {
            M[i] = m_val;
        }
    }
    
    int global_max = M[Z];
    
    // Base Case initialization at Length L = 1
    int prev = 1 % 2;
    dp[prev][Z][0].push_back({0, M[Z]});
    dp[prev][Z][1].push_back({0, M[Z]});
    
    // Bottom-Up Dynamic Programming over window length L
    for (int L = 2; L <= N; L++) {
        int curr = L & 1;
        prev = curr ^ 1;
        
        // Determine valid bounds for the interval [l, r] that MUST encapsulate Z
        int l_start = max(0, Z - L + 1);
        int l_end = min(Z, N - L);
        
        for (int l = l_start; l <= l_end; l++) {
            int r = l + L - 1;
            
            // 1. Compute pos = 0 (we just arrived at `l`)
            dp[curr][l][0].clear();
            if (l + 1 <= Z) {
                int d1 = X[l+1] - X[l];
                int d2 = X[r] - X[l];
                merge_and_pareto(dp[prev][l+1][0], d1, M[l],
                                 dp[prev][l+1][1], d2,
                                 dp[curr][l][0], global_max);
            }
            
            // 2. Compute pos = 1 (we just arrived at `r`)
            dp[curr][l][1].clear();
            if (r - 1 >= Z) {
                int d1 = X[r] - X[l];
                int d2 = X[r] - X[r-1];
                merge_and_pareto(dp[prev][l][0], d1, M[r],
                                 dp[prev][l][1], d2,
                                 dp[curr][l][1], global_max);
            }
        }
    }
    
    cout << global_max << "\n";
    
    return 0;
}