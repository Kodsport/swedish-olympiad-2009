#!/usr/bin/python3
# Edge-case generator: single-sign inputs, K >= N, N = 1, zeros, and
# anti-"nearest-first batching" cases with distinct spread-out distances.

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
mode = cmdlinearg('mode')
k = int(cmdlinearg('k'))

if mode == 'onesided':
    # All books strictly on one side of the origin (plus the extreme +-1000).
    sign = 1 if cmdlinearg('sign') == 'pos' else -1
    n = int(cmdlinearg('n'))
    xs = [1000] + [random.randint(1, 1000) for _ in range(n - 1)]
    xs = [sign * x for x in xs]
elif mode == 'antinearest':
    # Distinct distances on both sides, side sizes not divisible by K, so
    # batching trips from the nearest books instead of the farthest is
    # strictly suboptimal. farside says which side holds the unique maximum.
    npos = int(cmdlinearg('npos'))
    nneg = int(cmdlinearg('nneg'))
    dists = random.sample(range(1, 1000), npos + nneg)
    pos, neg = dists[:npos], dists[npos:]
    far = pos if cmdlinearg('farside') == 'pos' else neg
    far[far.index(max(far))] = 1000
    xs = pos + [-d for d in neg]
elif mode == 'singletrip':
    # K >= N: one trip per side suffices. Both sides nonempty.
    n = int(cmdlinearg('n'))
    xs = [1000, -1000] + [random.choice([-1, 1]) * random.randint(1, 1000) for _ in range(n - 2)]
elif mode == 'zeros':
    # Many books whose shelf is at the origin, mixed with normal books.
    n = int(cmdlinearg('n'))
    nzero = int(cmdlinearg('nzero'))
    xs = [0] * nzero + [random.choice([-1, 1]) * random.randint(1, 1000) for _ in range(n - nzero)]
elif mode == 'minimal':
    # N = 1.
    xs = [int(cmdlinearg('v'))]
else:
    assert 0

random.shuffle(xs)
print(len(xs), k)
for x in xs:
    print(x)
