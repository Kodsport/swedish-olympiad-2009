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

MAX_COORD = 10000

# Dense symmetric drops around 0 with unit spacing.
# This maximizes the search tree for 2^n brute-force solutions
# by creating many valid interleavings of left/right choices.
# With large m, both directions stay viable for many levels of
# the search tree, defeating pruning heuristics.

half = n // 2
other = n - half
drops = list(range(-half, 0)) + list(range(1, other + 1))

# Small random perturbations to create variety across seeds
# while preserving the dense symmetric structure
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

print(n, m)
for x in drops:
    print(x)
