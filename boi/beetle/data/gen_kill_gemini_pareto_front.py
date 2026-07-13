#!/usr/bin/python3

import sys


def cmdlinearg(name, default=None):
    for arg in sys.argv:
        if arg.startswith(name + "="):
            return arg.split("=", 1)[1]
    if default is None:
        print("missing parameter", name)
        sys.exit(1)
    return default


n = int(cmdlinearg("n"))
m = int(cmdlinearg("m"))
base = float(cmdlinearg("base", "1.0419"))
max_coord = int(cmdlinearg("max_coord", "10000"))

drops = set()
distance = 1

while distance <= max_coord and len(drops) < n:
    drops.add(distance)
    if len(drops) == n:
        break
    drops.add(-distance)

    next_distance = int(round(distance * base)) + 1
    if next_distance <= distance:
        next_distance = distance + 1
    distance = next_distance

# A few far-left padding points preserve more non-dominated states than
# filling the first holes near the origin.
padding = max_coord
while len(drops) < n and padding >= 1:
    candidate = -padding
    if candidate not in drops:
        drops.add(candidate)
    padding -= 1

if len(drops) < n:
    print("failed to generate enough coordinates", file=sys.stderr)
    sys.exit(1)

print(n, m)
for x in sorted(drops):
    print(x)
