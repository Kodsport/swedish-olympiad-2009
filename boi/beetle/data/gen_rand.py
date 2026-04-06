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

drops = []

MAX_COORD = 10**4

if mode == "random":
    drops = random.sample(range(-MAX_COORD, MAX_COORD+1), n)
elif mode == "positive":
    drops = random.sample(range(1, MAX_COORD+1), n)
elif mode == "negative":
    drops = random.sample(range(-MAX_COORD, 0), n)
else:
    assert 0

if int(cmdlinearg('zero', 0)):
    drops[0] = 0

random.shuffle(drops)

print(n, m)
for x in drops:
    print(x)
