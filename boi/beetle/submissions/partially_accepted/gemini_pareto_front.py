import sys

def solve():
    # Read all tokens from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    m = int(input_data[1])
    
    drops_input = []
    has_zero = False
    for i in range(n):
        x = int(input_data[2+i])
        drops_input.append(x)
        if x == 0:
            has_zero = True
            
    # Add artificial starting point if there isn't a drop at 0
    if not has_zero:
        drops_input.append(0)
        
    drops_input.sort()
    
    N = len(drops_input)
    X = drops_input
    
    # Establish original quantities of water at each index
    M = []
    Z = -1
    for i in range(N):
        if X[i] == 0:
            Z = i
            M.append(m if has_zero else 0)
        else:
            M.append(m)
            
    # dp[l][r] will store a tuple: (pareto_front_at_l, pareto_front_at_r)
    # where each pareto front is a list of (time, water) pairs.
    dp = [[([], []) for _ in range(N)] for __ in range(N)]
    
    # Base Case at the origin 0
    dp[Z][Z] = ([(0, M[Z])], [(0, M[Z])])
    
    # Track global maximum possible water that can be consumed
    max_ans = M[Z]
    
    # Bottom-Up Dynamic Programming (by length of interval L)
    for L in range(2, N + 1):
        # Determine valid intervals [l, r] that MUST contain the starting coordinate Z
        for l in range(max(0, Z - L + 1), min(Z + 1, N - L + 1)):
            r = l + L - 1
            
            # 1. Compute pos = 0 (we just arrived at `l`)
            pts0 = []
            if l + 1 <= Z:
                # Arrived at `l` from `l+1`
                d1 = X[l+1] - X[l]
                if dp[l+1][r][0]:
                    pts0.extend([(t + d1, w + (M[l] - t - d1 if M[l] > t + d1 else 0)) for t, w in dp[l+1][r][0]])
                
                # Arrived at `l` from `r`
                d2 = X[r] - X[l]
                if dp[l+1][r][1]:
                    pts0.extend([(t + d2, w + (M[l] - t - d2 if M[l] > t + d2 else 0)) for t, w in dp[l+1][r][1]])
                    
            pareto0 = []
            if pts0:
                # Merge into Pareto front: sort by shortest time first, then largest water to break ties
                pts0.sort(key=lambda x: (x[0], -x[1]))
                best_water = -1
                for t, w in pts0:
                    if w > best_water:
                        pareto0.append((t, w))
                        best_water = w
                        if w > max_ans:
                            max_ans = w
                            
            # 2. Compute pos = 1 (we just arrived at `r`)
            pts1 = []
            if r - 1 >= Z:
                # Arrived at `r` from `l`
                d1 = X[r] - X[l]
                if dp[l][r-1][0]:
                    pts1.extend([(t + d1, w + (M[r] - t - d1 if M[r] > t + d1 else 0)) for t, w in dp[l][r-1][0]])
                
                # Arrived at `r` from `r-1`
                d2 = X[r] - X[r-1]
                if dp[l][r-1][1]:
                    pts1.extend([(t + d2, w + (M[r] - t - d2 if M[r] > t + d2 else 0)) for t, w in dp[l][r-1][1]])
                    
            pareto1 = []
            if pts1:
                # Merge into Pareto front: sort by shortest time first, then largest water to break ties
                pts1.sort(key=lambda x: (x[0], -x[1]))
                best_water = -1
                for t, w in pts1:
                    if w > best_water:
                        pareto1.append((t, w))
                        best_water = w
                        if w > max_ans:
                            max_ans = w
                            
            dp[l][r] = (pareto0, pareto1)

    # tot_size = 0
    # for l in range(N):
    #     for r in range(l, N):
    #         tot_size += len(dp[l][r][0]) + len(dp[l][r][1])
    # print("Total size of all pareto fronts:", tot_size)
    # bins = N
    # bin_values = [0] * bins
    # for l in range(N):
    #     for r in range(l, N):
    #         toadd = len(dp[l][r][0]) + len(dp[l][r][1])
    #         bin_values[l] += toadd
    # print("Bin distribution of pareto front sizes:", bin_values)

    print(max_ans)

if __name__ == '__main__':
    solve()
