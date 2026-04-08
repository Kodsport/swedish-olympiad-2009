#!/usr/bin/python3
"""
Generator to create adversarial test data for beetle_js and joshua_cheese
with group 3 constraints (n<=100, m<=1000).

Both solutions use DFS with weak memoization. The key weakness exploited:
- beetle_js: single (lvl, drops) pair per state, incomparable pairs defeat pruning
- joshua_cheese: cache overwritten by last visitor, left-first DFS pollutes cache

Strategy: asymmetric placement with 40 left drops in 4 clusters at moderate
distances (60, 100, 265, 280 from origin) and 60 dense right drops near 0.
The DFS explores far-left paths first (expensive, late arrival), storing
poor cache values. Right-first paths arrive later but can't benefit from
the polluted cache, forcing re-exploration.

Grid-search optimized cluster positions achieve ~35M/23M recursion calls
for beetle_js/joshua_cheese respectively, making this ~200x harder than
random data.
"""

import sys
import random

def cmdlinearg(name, default=None):
    for arg in sys.argv:
        if arg.startswith(name + "="):
            return arg.split("=")[1]
    if default is None:
        print("missing parameter", name)
        sys.exit(1)
    return default

random.seed(int(cmdlinearg('seed', sys.argv[-1])))
n = int(cmdlinearg('n'))
m = int(cmdlinearg('m'))

MAX_COORD = 10000

# Grid-search optimized cluster positions for n=100, m=1000.
# 4 clusters on the left at distances 60, 100, 265, 280 from origin.
# Sizes: 14, 11, 9, 6 (more drops in nearer clusters).
# 60 dense right drops at 1-60.
clusters = [
    (-60, 14),   # near-left cluster
    (-100, 11),  # mid-left cluster
    (-265, 9),   # far-left cluster
    (-280, 6),   # farthest-left cluster
]

base_left = []
for center, size in clusters:
    base_left.extend(range(center, center - size, -1))

base_right = list(range(1, 61))

n_left_total = sum(s for _, s in clusters)
n_right_total = len(base_right)

if n >= n_left_total + n_right_total:
    drops = list(base_left) + list(base_right)
elif n <= n_right_total:
    drops = list(base_right[:n])
else:
    # Scale down: keep proportional left drops, fill remaining with right
    n_right = min(n_right_total, n * 3 // 5)
    n_left = n - n_right
    # Keep near clusters first, then far
    left = []
    for center, size in clusters:
        take = min(size, n_left - len(left))
        if take > 0:
            left.extend(range(center, center - take, -1))
    drops = list(left) + list(range(1, n_right + 1))

# Perturbation: move each drop by a small random amount for seed variety
used = set(drops)
perturbed = []
for d in drops:
    used.discard(d)
    moved = False
    for _ in range(5):
        delta = random.randint(-3, 3)
        new = d + delta
        if new != 0 and abs(new) <= MAX_COORD and new not in used:
            if (d < 0 and new < 0) or (d > 0 and new > 0):
                perturbed.append(new)
                used.add(new)
                moved = True
                break
    if not moved:
        perturbed.append(d)
        used.add(d)

drops = perturbed[:n]

# Ensure exactly n unique drops
drops = list(set(drops))
drops = [d for d in drops if d != 0 and abs(d) <= MAX_COORD]
while len(drops) < n:
    for c in range(1, MAX_COORD + 1):
        if c not in set(drops) and -c not in set(drops):
            drops.append(c)
            if len(drops) >= n:
                break
drops = drops[:n]

random.shuffle(drops)
print(n, m)
for x in drops:
    print(x)
