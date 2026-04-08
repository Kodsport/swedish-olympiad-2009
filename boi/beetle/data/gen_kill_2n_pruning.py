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

random.seed(int(cmdlinearg('seed', sys.argv[-1])))
n = int(cmdlinearg('n'))
m = int(cmdlinearg('m'))
base = float(cmdlinearg('base', '1.05'))

MAX_COORD = 10000

# Exponential spacing on both sides of origin.
# This creates drops at many distance scales, forcing the beetle
# to decide between collecting nearby guaranteed water vs rushing
# to far drops before they evaporate. This defeats pruning in
# 2^n brute-force solutions because exponentially many left/right
# interleavings produce near-optimal scores.

half = n // 2
other = n - half

left_drops = []
right_drops = []
d = 1
for i in range(half):
    left_drops.append(-d)
    d = max(d + 1, int(d * base) + 1)

d = 1
for i in range(other):
    right_drops.append(d)
    d = max(d + 1, int(d * base) + 1)

drops = left_drops + right_drops
drops = [p for p in drops if abs(p) <= MAX_COORD and p != 0]

# Small perturbations for variety across seeds
used = set(drops)
for i in range(len(drops)):
    for _ in range(3):
        delta = random.randint(-2, 2)
        new_val = drops[i] + delta
        if new_val != 0 and abs(new_val) <= MAX_COORD and new_val not in used:
            used.discard(drops[i])
            drops[i] = new_val
            used.add(new_val)
            break

random.shuffle(drops)
print(len(drops), m)
for x in drops:
    print(x)
