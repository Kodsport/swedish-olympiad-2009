#!/usr/bin/python3

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


# Band weights are convex (W[k] > W[k-1] + W[0]) so that a node first reached
# through a long band edge is improved once per shorter band, maximizing heap
# churn. Costs per unit (24 < 24.5 < 24.67 < 24.75) make single steps strictly
# cheapest, so dist(i, j) = 24*|i-j|: distances grow with label difference,
# which is the worst case for per-pair Dijkstras that stop at the target.
def banded(n, m, rng):
    W = [24, 49, 74, 99]
    edges = [(i, i + 1, W[0]) for i in range(1, n)]
    for k in range(2, 5):
        if len(edges) >= m:
            break
        band = [(i, i + k, W[k - 1]) for i in range(1, n - k + 1)]
        take = min(len(band), m - len(edges))
        if take < len(band):
            band = rng.sample(band, take)
        edges += band
    assert len(edges) == m, "m out of range for banded mode"
    return edges


# Even cycle of length 2L with an arm of `arm` nodes at two antipodal points;
# the diameter runs between the two arm tips (L + 2*arm edges of weight 50).
# Started anywhere in the middle of either half-cycle, "Dijkstra from s, then
# Dijkstra from the farthest node found" walks to the antipodal cycle node
# (eccentricity L) instead of an arm tip and answers 50*L, missing the true
# diameter 50*(L + 2*arm). Labels in those windows come first so that node 1
# is always such a start.
def antisweep(n, m, rng):
    assert m == n and n % 2 == 0 and n >= 16, "antisweep needs m == n, even n >= 16"
    arm = max(2, n // 20)
    L = (n - 2 * arm) // 2

    positions = []  # (position id) -> neighbors come later; build edge list on positions
    cyc = [("c", i) for i in range(2 * L)]
    armx = [("x", i) for i in range(1, arm + 1)]
    army = [("y", i) for i in range(1, arm + 1)]

    pos_edges = []
    for i in range(2 * L):
        pos_edges.append((("c", i), ("c", (i + 1) % (2 * L))))
    prev = ("c", 0)
    for p in armx:
        pos_edges.append((prev, p))
        prev = p
    prev = ("c", L)
    for p in army:
        pos_edges.append((prev, p))
        prev = p

    windows = []
    for i in range(arm + 1, L - arm):
        windows.append(("c", i))
        windows.append(("c", i + L))
    rest = [p for p in cyc + armx + army if p not in set(windows)]
    rng.shuffle(windows)
    rng.shuffle(rest)
    label = {p: idx + 1 for idx, p in enumerate(windows + rest)}

    return [(label[p], label[q], 50) for p, q in pos_edges]


# Random clusters strung along a path: within a cluster the graph is a random
# expander (large Dijkstra frontier, expensive heap ops); globally distances
# grow with cluster index, and labels follow cluster order, so per-pair
# Dijkstras that stop at the target must settle ~2*|cluster gap| clusters per
# pair — the worst case for them, combined with the expensive local structure.
def clustered(n, m, rng):
    s = 50
    assert n % s == 0, "clustered mode needs n divisible by 50"
    c = n // s
    clusters = [list(range(i * s + 1, (i + 1) * s + 1)) for i in range(c)]

    edges = set()
    def add(a, b, w):
        if a > b:
            a, b = b, a
        if (a, b) not in {e[:2] for e in edges}:
            edges.add((a, b, w))

    # spanning path within each cluster, plus bridges between adjacent clusters
    for cl in clusters:
        perm = cl[:]
        rng.shuffle(perm)
        for x, y in zip(perm, perm[1:]):
            add(x, y, rng.randint(1, 100))
    for i in range(c - 1):
        for _ in range(3):
            add(rng.choice(clusters[i]), rng.choice(clusters[i + 1]), rng.randint(90, 100))
    while len(edges) < m:
        cl = rng.randrange(c)
        a, b = rng.sample(clusters[cl], 2)
        add(a, b, rng.randint(1, 100))
    return sorted(edges)


def randgraph(n, m, rng):
    edges = set()
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    for i in range(1, n):
        a, b = perm[rng.randrange(i)], perm[i]
        edges.add((min(a, b), max(a, b)))
    while len(edges) < m:
        a, b = rng.sample(range(1, n + 1), 2)
        edges.add((min(a, b), max(a, b)))
    return [(a, b, rng.randint(1, 100)) for a, b in edges]


def path(n, m, rng):
    assert m == n - 1, "path mode needs m == n-1"
    return [(i, i + 1, rng.randint(1, 100)) for i in range(1, n)]


seed = int(cmdlinearg("seed", sys.argv[-1]))
rng = random.Random(seed)
mode = cmdlinearg("mode")
n = int(cmdlinearg("n"))
m = int(cmdlinearg("m"))

edges = {"clustered": clustered, "banded": banded, "antisweep": antisweep, "random": randgraph, "path": path}[mode](n, m, rng)

rng.shuffle(edges)
out = [f"{n}\n{m}\n"]
for a, b, w in edges:
    if rng.random() < 0.5:
        a, b = b, a
    out.append(f"{a} {b} {w}\n")
sys.stdout.write("".join(out))
