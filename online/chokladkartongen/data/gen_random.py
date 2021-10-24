#!/usr/bin/env python3

import sys
import random

def cmdlinearg(name, default=None):
    for arg in sys.argv:
        if arg.startswith(name + "="):
            return arg.split("=")[1]
    assert default is not None, name
    return default

seed = int(cmdlinearg('seed', sys.argv[-1]))
n = int(cmdlinearg('n'))
r = int(cmdlinearg('r'))

random.seed(seed)

print(n)
print(*[random.randint(1, r) for _ in range(n)])
