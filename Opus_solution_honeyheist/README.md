# Honey Heist - Solution Explanation

## Problem Summary

A scout ant (ox67) needs to navigate through a hexagonal honeycomb grid from cell **A** to cell **B**. The ant can chew through at most **N** cells, and some cells are blocked with hardened wax. We need to find the minimum number of cells **K** required to reach the honey, or report "No" if it's impossible.

---

## Understanding the Hexagonal Grid

### Grid Structure

The honeycomb is a **hexagonal grid** with edge length **R**. The total number of cells is calculated as:

$$\text{Total Cells} = R^3 - (R-1)^3$$

For example, with R=4: $4^3 - 3^3 = 64 - 27 = 37$ cells.

### Row Layout

The grid has **2R - 1** rows arranged in a diamond pattern:

```
For R = 4:
Row 0:    ⬡ ⬡ ⬡ ⬡           (4 cells)
Row 1:   ⬡ ⬡ ⬡ ⬡ ⬡          (5 cells)
Row 2:  ⬡ ⬡ ⬡ ⬡ ⬡ ⬡         (6 cells)
Row 3: ⬡ ⬡ ⬡ ⬡ ⬡ ⬡ ⬡        (7 cells) ← Middle row (2R-1 cells)
Row 4:  ⬡ ⬡ ⬡ ⬡ ⬡ ⬡         (6 cells)
Row 5:   ⬡ ⬡ ⬡ ⬡ ⬡          (5 cells)
Row 6:    ⬡ ⬡ ⬡ ⬡           (4 cells)
```

Row lengths follow the pattern: **R, R+1, R+2, ..., 2R-1, ..., R+2, R+1, R**

### Cell Numbering

Cells are numbered in **row-major order** starting from 1:

```
For R = 4:
         1   2   3   4
       5   6   7   8   9
     10  11  12  13  14  15
   16  17  18  19  20  21  22
     23  24  25  26  27  28
       29  30  31  32  33
         34  35  36  37
```

---

## Hexagonal Neighbor Relationships

### The Key Challenge

In a hexagonal grid, each cell has up to **6 neighbors**. The tricky part is that neighbor relationships depend on whether the row is in the **upper half** (expanding) or **lower half** (shrinking) of the grid.

### Neighbor Rules

For a cell at position (row, col):

#### 1. Same Row Neighbors
- **Left**: (row, col-1) if col > 0
- **Right**: (row, col+1) if col < row_length - 1

#### 2. Upper Row Neighbors (row - 1)

**If current row ≤ middle row** (upper half, rows expanding):
- Previous row is shorter
- Upper neighbors: (row-1, col-1) and (row-1, col)

**If current row > middle row** (lower half, rows shrinking):
- Previous row is longer  
- Upper neighbors: (row-1, col) and (row-1, col+1)

#### 3. Lower Row Neighbors (row + 1)

**If current row < middle row** (upper half):
- Next row is longer
- Lower neighbors: (row+1, col) and (row+1, col+1)

**If current row ≥ middle row** (lower half):
- Next row is shorter
- Lower neighbors: (row+1, col-1) and (row+1, col)

### Visual Example

```
Upper half expansion:         Lower half contraction:
    A   B                         A   B   C
   C   D   E                       D   E

Cell D's upper neighbors:     Cell D's upper neighbors:
  A and B                       A and B
Cell D's lower neighbors:     Cell D's lower neighbors:
  Would be longer row           Would be shorter row
```

---

## Algorithm: Breadth-First Search (BFS)

### Why BFS?

BFS is ideal for finding the **shortest path in an unweighted graph**. Since each cell transition has equal cost (1 cell), BFS guarantees we find the minimum number of cells to traverse.

### Algorithm Steps

```
1. Build adjacency list for all cells
2. Initialize:
   - visited = {start_cell}
   - queue = [(start_cell, distance=1)]

3. While queue is not empty:
   a. Dequeue (current_cell, distance)
   b. For each neighbor of current_cell:
      - If neighbor is the target: return distance + 1
      - If neighbor not visited and not blocked:
        * Mark as visited
        * Enqueue (neighbor, distance + 1)

4. If queue exhausted: return -1 (no path)
```

### Time Complexity

- **O(V + E)** where V = number of cells, E = number of edges
- V = R³ - (R-1)³ ≤ 20³ - 19³ = 1141 cells (max)
- Each cell has at most 6 neighbors, so E ≤ 6V
- Very efficient for the given constraints

### Space Complexity

- **O(V)** for the adjacency list, visited set, and queue

---

## Implementation Details

### Data Structures

1. **`id_to_pos`**: Maps cell ID → (row, col)
2. **`pos_to_id`**: Maps (row, col) → cell ID
3. **`adj`**: Adjacency list mapping cell ID → list of neighbor IDs

### Key Functions

| Function | Purpose |
|----------|---------|
| `get_row_lengths(R)` | Calculate length of each row |
| `build_cell_info(R)` | Create coordinate mappings |
| `get_neighbors(...)` | Find all neighbors for a cell |
| `build_adjacency_list(R)` | Build complete graph |
| `bfs_shortest_path(...)` | Find shortest path avoiding blocked cells |

---

## Example Walkthrough

### Sample Input 1
```
6 6 1 45 11
15 16 17 19 26 27 52 53 58 59 60
```

**Parameters:**
- R = 6 (edge length)
- N = 6 (max cells ant can chew)
- A = 1 (start cell)
- B = 45 (target cell)
- Blocked cells: {15, 16, 17, 19, 26, 27, 52, 53, 58, 59, 60}

**BFS Execution:**
1. Start at cell 1
2. Explore neighbors, avoiding blocked cells
3. Find shortest path of length 6

**Output:** `6` (K=6 ≤ N=6, so path is valid)

### Sample Input 2
```
6 3 1 45 11
15 16 17 19 26 27 52 53 58 59 60
```

Same blocked cells, but N=3 (max 3 cells).

**Output:** `No` (K=6 > N=3, ant not strong enough)

---

## Edge Cases Handled

1. **Start equals End**: Return K=1
2. **Start or End blocked**: Return "No"
3. **No path exists**: Return "No"
4. **Path exists but K > N**: Return "No"

---

## Usage

```bash
# Run with input from stdin
python honey_heist.py < input.txt

# Or interactively
python honey_heist.py
6 6 1 45 11
15 16 17 19 26 27 52 53 58 59 60
```

---

## Complexity Summary

| Aspect | Complexity |
|--------|------------|
| Grid Construction | O(V) |
| Adjacency List | O(V) |
| BFS | O(V + E) = O(V) |
| **Total** | **O(V)** where V = R³ - (R-1)³ |

For maximum R=20: V ≤ 1141 cells, making this extremely efficient.
