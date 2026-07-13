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

def pad_drops(drops, n):
    """Pad drops list to exactly n elements."""
    drops = list(set(drops) - {0})
    drops = [d for d in drops if -MAX_COORD <= d <= MAX_COORD]
    used = set(drops)
    for c in range(1, MAX_COORD + 1):
        if len(drops) >= n:
            break
        if c not in used:
            drops.append(c)
            used.add(c)
        if len(drops) >= n:
            break
        if -c not in used:
            drops.append(-c)
            used.add(-c)
    return drops[:n]


if mode == "kill_cheese":
    # Drops with mixed spacing: some very close to 0, some far away.
    # This defeats the heuristic memoization in cheese-style solutions
    # by creating many paths to each DP state with different arrival times.
    near = int(cmdlinearg('near', str(n // 4)))
    far_start = int(cmdlinearg('far_start', '500'))
    far_step = int(cmdlinearg('far_step', '100'))

    half = n // 2
    left_near = min(near, half)
    right_near = min(near, n - half)
    left_far = half - left_near
    right_far = (n - half) - right_near

    drops = []
    drops.extend([-i for i in range(1, left_near + 1)])
    drops.extend([i for i in range(1, right_near + 1)])

    for i in range(left_far):
        val = -(far_start + i * far_step)
        if val >= -MAX_COORD:
            drops.append(val)
    for i in range(right_far):
        val = far_start + i * far_step
        if val <= MAX_COORD:
            drops.append(val)

    drops = pad_drops(drops, n)

elif mode == "kill_cheese_hard":
    # Optimized adversarial placement found via hill climbing.
    # Base positions create multi-scale cache thrashing in cheese-style
    # memoization. Dense asymmetric near-0 cluster + scattered mid/far drops.
    # Small perturbations (±3) preserve the adversarial property robustly.
    base = [-9882, -9741, -9229, -9119, -8525, -8517, -6385, -6320, -5363,
            -5260, -3028, -1621, -1554, -1301, -1299, -1290, -1163, -1106,
            -988, -816, -555, -499, -428, -351, -126, -102, -76, -66, -64,
            -57, -52, -51, -48, -42, -41, -29, -20, -16, -13, -12, -11, -8,
            -7, -6, -4, -3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14,
            16, 17, 18, 19, 22, 23, 76, 179, 199, 201, 229, 237, 274, 275,
            287, 313, 369, 373, 674, 1735, 2090, 2470, 2766, 2888, 3024,
            3028, 3641, 3717, 4045, 4377, 4602, 5260, 5717, 6320, 6671,
            6721, 7039, 7298, 7592, 7711, 9463]
    assert len(base) == 100

    if n > 100:
        # For n > 100: use the base pattern and pad with additional drops
        drops = list(base)
    elif n == 100:
        drops = list(base)
    else:
        # For n < 100: take a subset keeping the near-0 cluster intact
        near_drops = [d for d in base if abs(d) <= 25]
        far_drops = [d for d in base if abs(d) > 25]
        random.shuffle(far_drops)
        drops = near_drops + far_drops[:n - len(near_drops)]

    # Apply small perturbations for variety across seeds
    perturb = int(cmdlinearg('perturb', '3'))
    for i in range(len(drops)):
        delta = random.randint(-perturb, perturb)
        new_val = drops[i] + delta
        if new_val != 0 and abs(new_val) <= MAX_COORD and new_val not in set(drops[:i] + drops[i+1:]):
            drops[i] = new_val

    drops = pad_drops(drops, n)

else:
    assert False, f"Unknown mode: {mode}"

random.shuffle(drops)

print(n, m)
for x in drops:
    print(x)
