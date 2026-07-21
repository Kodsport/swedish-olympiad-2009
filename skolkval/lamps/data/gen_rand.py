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


from random import randint
random.seed(int(cmdlinearg('seed', sys.argv[-1])))
mode = cmdlinearg('mode')


def gen(maxH):
    # rejection sample until break-even happens within maxH hours
    while True:
        h, p = randint(1, 24), randint(1, 200)
        d = 1
        while 500000 * ((d*h + 999) // 1000) + 49*d*h*p <= 6000000:
            d += 1
        if d*h <= maxH:
            return h, p

if mode=="noswitch":
    print(*gen(1000))
elif mode=="random":
    print(*gen(8000))
else:
    assert 0
