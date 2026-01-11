"""
Lost In The Woods - Expected Hitting Time Problem

This is a random walk on a graph where we need to find the expected number
of steps to reach the exit (node N-1) starting from node 0.

Mathematical approach:
- Let E[i] = expected time to reach exit from node i
- E[N-1] = 0 (base case: already at exit)
- For other nodes: E[i] = 1 + (1/degree(i)) * sum(E[j] for neighbors j)

This creates a system of linear equations: A * E = b
"""

import numpy as np
from collections import defaultdict


def solve():
    # Read input
    line = input().split()
    N, M = int(line[0]), int(line[1])
    
    # Build adjacency list
    adj = defaultdict(list)
    for _ in range(M):
        edge = input().split()
        k, l = int(edge[0]), int(edge[1])
        adj[k].append(l)
        adj[l].append(k)
    
    # We need to solve for E[0], E[1], ..., E[N-2]
    # E[N-1] = 0 (exit node)
    
    # Set up the system of equations
    # For node i (i != N-1):
    #   E[i] = 1 + (1/deg[i]) * sum(E[j] for j in neighbors)
    #   E[i] - (1/deg[i]) * sum(E[j]) = 1
    #   deg[i]*E[i] - sum(E[j]) = deg[i]
    
    # Number of unknowns is N-1 (all nodes except exit)
    n_unknowns = N - 1
    
    # Create coefficient matrix A and constant vector b
    A = np.zeros((n_unknowns, n_unknowns))
    b = np.zeros(n_unknowns)
    
    for i in range(N - 1):  # For each non-exit node
        degree = len(adj[i])
        
        # Coefficient for E[i] is 1
        A[i][i] = 1.0
        
        # Coefficient for each neighbor E[j] is -1/degree
        for j in adj[i]:
            if j != N - 1:  # Only if neighbor is not the exit
                A[i][j] = -1.0 / degree
        
        # The constant term is 1
        # But if neighbor is the exit (N-1), E[N-1] = 0, so it contributes 0
        b[i] = 1.0
    
    # Solve the system A * E = b
    E = np.linalg.solve(A, b)
    
    # The answer is E[0]
    print(f"{E[0]:.6f}")


if __name__ == "__main__":
    solve()
