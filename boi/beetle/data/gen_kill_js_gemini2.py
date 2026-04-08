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
mode = cmdlinearg('mode')

MAX_COORD = 10000

if mode == 'kill_js':
    # Hill-climbed positions optimized to maximize beetle_js.cc recursion calls.
    # Dense cluster near origin on right (positions 2-90 with some gaps) +
    # scattered far drops on left + a few far drops on right.
    base = [
        -10000, -8939, -7943, -7219, -7000, -6857, -6000, -5345, -5000,
        -4215, -3249, -3084, -3000, -2944, -1365, -1000, -954, -952, -927, -860,
        2, 3, 4, 5, 8, 9, 10, 14, 15, 16, 17, 19, 20, 21, 22, 23, 25, 26,
        27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44,
        45, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
        63, 64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 75, 77, 78, 79, 83, 84,
        85, 86, 87, 88, 90, 4374, 5668, 5754, 7320, 8746, 9931
    ]

    # Apply small perturbations based on seed for variety
    used = set(base)
    for i in range(len(base)):
        for _ in range(3):
            delta = random.randint(-3, 3)
            new_val = base[i] + delta
            if new_val != 0 and abs(new_val) <= MAX_COORD and new_val not in used:
                used.discard(base[i])
                base[i] = new_val
                used.add(new_val)
                break

    drops = base[:n]

elif mode == 'kill_gemini2':
    # Exponential spacing on both sides of origin.
    # Creates many non-dominated Pareto frontier entries in the
    # gemini2 DFS, defeating its Pareto domination pruning.
    base = float(cmdlinearg('base', '1.04'))

    drops = []
    d = 1
    for _ in range(n * 2):
        drops.append(d)
        drops.append(-d)
        d = int(d * base) + 1

    drops = sorted(set(drops))
    drops = [p for p in drops if abs(p) <= MAX_COORD and p != 0][:n]

    # Small perturbations for variety
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

else:
    print(f"Unknown mode: {mode}", file=sys.stderr)
    sys.exit(1)

random.shuffle(drops)
print(len(drops), m)
for x in drops:
    print(x)
