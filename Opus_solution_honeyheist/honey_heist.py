#!/usr/bin/env python3
"""
Honey Heist - Hexagonal Grid Shortest Path Problem
Solution using BFS on a hexagonal honeycomb grid.
"""

from collections import deque


def get_row_lengths(R):
    """
    Calculate the length of each row in a hexagonal grid with edge length R.
    
    For R=4, rows have lengths: [4, 5, 6, 7, 6, 5, 4]
    Total rows = 2R - 1
    """
    lengths = []
    # Upper half (including middle row): R, R+1, R+2, ..., 2R-1
    for i in range(R):
        lengths.append(R + i)
    # Lower half: 2R-2, 2R-3, ..., R
    for i in range(R - 2, -1, -1):
        lengths.append(R + i)
    return lengths


def build_cell_info(R):
    """
    Build mappings between cell IDs and their (row, col) positions.
    
    Returns:
        id_to_pos: dict mapping cell_id -> (row, col)
        pos_to_id: dict mapping (row, col) -> cell_id
        row_lengths: list of row lengths
    """
    row_lengths = get_row_lengths(R)
    id_to_pos = {}
    pos_to_id = {}
    
    cell_id = 1
    for row, length in enumerate(row_lengths):
        for col in range(length):
            id_to_pos[cell_id] = (row, col)
            pos_to_id[(row, col)] = cell_id
            cell_id += 1
    
    return id_to_pos, pos_to_id, row_lengths


def get_neighbors(row, col, row_lengths, pos_to_id, R):
    """
    Get all valid neighboring cell IDs for a cell at (row, col).
    
    In a hexagonal grid with offset coordinates, neighbors depend on 
    whether we're in the upper half (expanding rows) or lower half (shrinking rows).
    
    For a cell, the 6 potential neighbors are:
    - Same row: left (col-1), right (col+1)
    - Row above and row below: depends on grid structure
    """
    neighbors = []
    total_rows = len(row_lengths)
    middle_row = R - 1  # 0-indexed middle row
    
    # Same row neighbors (left and right)
    if col > 0:
        neighbors.append((row, col - 1))
    if col < row_lengths[row] - 1:
        neighbors.append((row, col + 1))
    
    # Upper neighbor row
    if row > 0:
        prev_len = row_lengths[row - 1]
        curr_len = row_lengths[row]
        
        if row <= middle_row:
            # Current row is in upper half (rows are expanding)
            # Previous row is shorter, offset by -1
            # Neighbors above: col-1 and col (in prev row's indexing)
            for dc in [-1, 0]:
                nc = col + dc
                if 0 <= nc < prev_len:
                    neighbors.append((row - 1, nc))
        else:
            # Current row is in lower half (rows are shrinking)
            # Previous row is longer, offset by +1
            # Neighbors above: col and col+1 (in prev row's indexing)
            for dc in [0, 1]:
                nc = col + dc
                if 0 <= nc < prev_len:
                    neighbors.append((row - 1, nc))
    
    # Lower neighbor row
    if row < total_rows - 1:
        next_len = row_lengths[row + 1]
        curr_len = row_lengths[row]
        
        if row < middle_row:
            # Current row is in upper half (next row is longer)
            # Neighbors below: col and col+1 (in next row's indexing)
            for dc in [0, 1]:
                nc = col + dc
                if 0 <= nc < next_len:
                    neighbors.append((row + 1, nc))
        else:
            # Current row is at or past middle (next row is shorter)
            # Neighbors below: col-1 and col (in next row's indexing)
            for dc in [-1, 0]:
                nc = col + dc
                if 0 <= nc < next_len:
                    neighbors.append((row + 1, nc))
    
    # Convert positions to cell IDs
    neighbor_ids = []
    for pos in neighbors:
        if pos in pos_to_id:
            neighbor_ids.append(pos_to_id[pos])
    
    return neighbor_ids


def build_adjacency_list(R):
    """
    Build complete adjacency list for the hexagonal grid.
    
    Returns:
        adj: dict mapping cell_id -> list of neighbor cell_ids
    """
    id_to_pos, pos_to_id, row_lengths = build_cell_info(R)
    
    adj = {}
    for cell_id, (row, col) in id_to_pos.items():
        adj[cell_id] = get_neighbors(row, col, row_lengths, pos_to_id, R)
    
    return adj


def bfs_shortest_path(adj, start, end, blocked):
    """
    Find shortest path from start to end using BFS, avoiding blocked cells.
    
    Args:
        adj: adjacency list
        start: starting cell ID
        end: target cell ID  
        blocked: set of blocked cell IDs
        
    Returns:
        K: number of cells in path (including start and end), or -1 if no path
    """
    if start == end:
        return 1
    
    if start in blocked or end in blocked:
        return -1
    
    visited = {start}
    queue = deque([(start, 1)])  # (cell_id, distance)
    
    while queue:
        current, dist = queue.popleft()
        
        for neighbor in adj[current]:
            if neighbor == end:
                return dist + 1
            
            if neighbor not in visited and neighbor not in blocked:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1  # No path found


def solve():
    """Main solution function."""
    # Parse first line
    line1 = input().split()
    R = int(line1[0])
    N = int(line1[1])
    A = int(line1[2])
    B = int(line1[3])
    X = int(line1[4])
    
    # Parse blocked cells (second line)
    blocked = set()
    if X > 0:
        line2 = input().split()
        for cell_str in line2:
            blocked.add(int(cell_str))
    
    # Build grid adjacency
    adj = build_adjacency_list(R)
    
    # Find shortest path
    K = bfs_shortest_path(adj, A, B, blocked)
    
    # Output result
    if K == -1 or K > N:
        print("No")
    else:
        print(K)


if __name__ == "__main__":
    solve()
