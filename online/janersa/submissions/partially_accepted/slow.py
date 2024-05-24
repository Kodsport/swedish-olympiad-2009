#!/usr/bin/python3
import sys
import heapq
from collections import defaultdict, deque

# Constants
inf = int(1e9)

# Helper functions
def read():
    return sys.stdin.read().split()

def write(a):
    print(a)

def ceildiv(x, y):
    return (x + y - 1) // y

def shortest(edges, start, target, n):
    import math
    # Initialize distances with infinity
    d = [math.inf] * (n + 1)
    d[start] = 0
    
    # List to explore nodes
    to_explore = [(0, start)]
    
    while to_explore:
        # Find the node with the smallest distance
        to_explore.sort()
        curr_dist, curr = to_explore.pop(0)
        
        # Explore neighbors
        for length, neighbor in edges[curr]:
            new_cost = length + d[curr]
            if new_cost < d[neighbor]:
                d[neighbor] = new_cost
                to_explore.append((new_cost, neighbor))
    
    return d[target]


def main():
    input_data = read()
    idx = 0

    n = int(input_data[idx])
    idx += 1
    v = int(input_data[idx])
    idx += 1

    edges = defaultdict(set)
    for _ in range(v):
        houseA = int(input_data[idx])
        idx += 1
        houseB = int(input_data[idx])
        idx += 1
        length = int(input_data[idx])
        idx += 1

        edges[houseA].add((length, houseB))
        edges[houseB].add((length, houseA))

    longest = -1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                continue
            dist = shortest(edges, i, j, n)
            longest = max(longest, dist)


    write(f"{longest * 100}")

if __name__ == "__main__":
    main()
