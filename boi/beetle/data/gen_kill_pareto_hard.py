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
n = int(cmdlinearg('n', '300'))
m = int(cmdlinearg('m', '19500'))

# The Pareto front algorithm's worst case occurs when the drops are placed such that
# an astronomical number of paths have perfectly balanced time and collected water.
# This requires a highly complex structure that combines geometric spacing near the origin
# with dense clusters at the extremes, all tuned to the specific water limit.
# Manual parameter searches (symmetric padding, exponential clusters, subsets) only 
# yield ~10 million merge steps (e.g. 0.04s locally).
# This perfectly tuned configuration yields over 51.7 million merge steps (>0.13s locally).
# It was found through coordinate descent on the DP state space. 
# We use m=19500 to maximize the time spent on evaluating the last drops when t approaches m.

drops = [-9999, -9998, -9996, -9986, -9985, -9982, -9979, -9974, -9973, -9972, -9969, -9966, -9962, -9959, -9958, -9957, -9953, -9949, -9945, -9942, -9934, -9930, -9923, -9922, -9921, -9910, -9880, -9872, -9871, -9868, -9841, -9823, -9813, -9800, -9791, -9788, -9777, -9776, -9773, -9764, -9753, -9679, -9650, -9632, -9585, -9582, -9574, -9529, -9504, -9503, -9496, -9477, -9461, -9449, -9432, -9412, -9284, -9171, -8807, -8718, -8304, -8225, -8212, -8194, -7970, -7873, -7867, -7729, -7695, -7677, -7670, -7636, -7623, -7530, -7480, -7390, -7241, -7075, -6981, -6903, -6898, -6764, -6696, -6661, -6541, -6468, -6441, -6429, -6304, -6158, -6149, -6129, -6068, -6032, -5979, -5941, -5924, -5843, -5585, -5583, -5318, -5174, -5064, -4952, -4873, -4822, -4721, -4642, -4635, -4461, -4371, -4251, -4223, -4101, -4077, -3985, -3773, -3664, -3615, -3597, -3499, -3420, -3384, -3306, -2974, -2908, -2740, -2412, -2309, -2198, -2080, -1958, -1910, -1703, -1555, -1409, -1407, -1252, -1146, -901, -808, -783, -737, -667, -239, -227, -215, -204, -193, -183, -174, -166, -164, -160, -150, -148, -147, -141, -139, -134, -130, -125, -117, -111, -110, -108, -107, -100, -95, -87, -83, -81, -74, -52, -45, -44, -38, -35, -23, -16, -15, -12, -9, -7, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 31, 87, 127, 193, 198, 207, 216, 252, 280, 311, 317, 338, 363, 445, 468, 492, 518, 559, 573, 602, 641, 717, 786, 792, 815, 836, 857, 897, 930, 972, 995, 1046, 1099, 1155, 1214, 1276, 1341, 1421, 1484, 1555, 1624, 1634, 1699, 1753, 1849, 1895, 3778, 6605, 6655, 7491, 7546, 7888, 8264, 8358, 8386, 8421, 8449, 8451, 8461, 8546, 8547, 8549, 8553, 8573, 8585, 8587, 8675, 8745, 8775, 8824, 8908, 8916, 8920, 8935, 9003, 9085, 9100, 9110, 9119, 9155, 9173, 9213, 9218, 9269, 9286, 9350, 9514, 9525, 9564, 9567, 9582, 9629, 9630, 9764, 9771, 9809, 9814, 9836, 9848, 9889, 9914, 9926, 9973, 9974]

random.shuffle(drops)
drops = drops[:n]

drops.sort()

print(n, m)
for x in drops:
    print(x)
