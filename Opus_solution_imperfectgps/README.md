# Imperfect GPS - Solution

## Problem Overview

Personal GPS receivers track runners by recording positions periodically rather than continuously. This sampling approach causes the GPS to potentially underestimate the actual distance run, as it assumes straight-line movement between recorded positions.

### Problem Statement

Given:
- A sequence of waypoints with coordinates and timestamps representing the actual running path
- A GPS sampling interval `t` (in seconds)

Calculate:
- The percentage of actual run distance that is "lost" (underestimated) by the GPS

### Key Constraints
- The GPS records at time 0, then every `t` seconds, and always at the end
- The runner moves at constant speed in straight lines between waypoints
- Output must be accurate within 10⁻⁵

---

## Solution Approach

### High-Level Algorithm

The solution follows these main steps:

1. **Calculate Actual Distance**: Sum the Euclidean distances between consecutive waypoints
2. **Generate GPS Sample Times**: Create timestamps when GPS would record (0, t, 2t, ..., end_time)
3. **Interpolate GPS Positions**: For each sample time, find the runner's exact position using linear interpolation
4. **Calculate GPS Distance**: Sum distances between consecutive GPS-recorded positions
5. **Compute Percentage Lost**: `(actual_distance - gps_distance) / actual_distance × 100`

---

## Detailed Algorithm Steps

### Step 1: Parse Input

Read the input data:
- First line: `n` (number of waypoints) and `t` (GPS interval)
- Next `n` lines: Each contains `x_i`, `y_i`, `t_i` (coordinates and time for waypoint i)

Store waypoints as tuples: `(x, y, time)`

### Step 2: Calculate Actual Running Distance

The actual path consists of straight-line segments between consecutive waypoints.

For each pair of consecutive waypoints $(x_1, y_1)$ and $(x_2, y_2)$:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

Sum all segment distances to get the total actual distance.

### Step 3: Generate GPS Sample Times

Create a list of times when the GPS records a position:
- Start at time 0
- Add times: `t, 2t, 3t, ...` while `< end_time`
- Always include `end_time` (even if not a multiple of `t`)

**Example:** If `t = 2` and `end_time = 11`:
- GPS times: `[0, 2, 4, 6, 8, 10, 11]`

### Step 4: Linear Interpolation for GPS Positions

For each GPS sample time τ, determine the runner's position:

1. **Find the segment**: Locate waypoints $P_1 = (x_1, y_1, t_1)$ and $P_2 = (x_2, y_2, t_2)$ where $t_1 \leq \tau \leq t_2$

2. **Calculate interpolation ratio**:
   $$\text{ratio} = \frac{\tau - t_1}{t_2 - t_1}$$

3. **Compute interpolated position**:
   $$x = x_1 + \text{ratio} \times (x_2 - x_1)$$
   $$y = y_1 + \text{ratio} \times (y_2 - y_1)$$

This gives the exact position assuming constant-speed linear motion between waypoints.

### Step 5: Calculate GPS-Measured Distance

Using the interpolated GPS positions, calculate the distance the GPS measures:
- Sum Euclidean distances between consecutive GPS-recorded positions
- This represents what the GPS "thinks" the distance is

### Step 6: Compute Percentage Lost

The percentage of distance lost due to GPS sampling:

$$\text{Percentage Lost} = \frac{\text{Actual Distance} - \text{GPS Distance}}{\text{Actual Distance}} \times 100$$

---

## Example Walkthrough

### Input
```
6 2
0 0 0
0 3 3
-2 5 5
0 7 7
2 5 9
0 3 11
```

### Step-by-Step Execution

#### 1. Actual Path
Waypoints:
- (0, 0) at t=0
- (0, 3) at t=3
- (-2, 5) at t=5
- (0, 7) at t=7
- (2, 5) at t=9
- (0, 3) at t=11

**Actual distances:**
- (0,0) → (0,3): $\sqrt{0^2 + 3^2} = 3.0$
- (0,3) → (-2,5): $\sqrt{4 + 4} = 2.828...$
- (-2,5) → (0,7): $\sqrt{4 + 4} = 2.828...$
- (0,7) → (2,5): $\sqrt{4 + 4} = 2.828...$
- (2,5) → (0,3): $\sqrt{4 + 4} = 2.828...$

**Total actual distance:** ≈ 14.313708 units

#### 2. GPS Sample Times
With t=2 and end_time=11: `[0, 2, 4, 6, 8, 10, 11]`

#### 3. GPS Positions (via interpolation)

| Time | Position Calculation | GPS Position |
|------|---------------------|--------------|
| 0 | Start point | (0, 0) |
| 2 | 2/3 along (0,0)→(0,3) | (0, 2) |
| 4 | 1/2 along (0,3)→(-2,5) | (-1, 4) |
| 6 | 1/2 along (-2,5)→(0,7) | (-1, 6) |
| 8 | 1/2 along (0,7)→(2,5) | (1, 6) |
| 10 | 1/2 along (2,5)→(0,3) | (1, 4) |
| 11 | End point | (0, 3) |

#### 4. GPS Distance
- (0,0) → (0,2): 2.0
- (0,2) → (-1,4): $\sqrt{1 + 4} = 2.236...$
- (-1,4) → (-1,6): 2.0
- (-1,6) → (1,6): 2.0
- (1,6) → (1,4): 2.0
- (1,4) → (0,3): $\sqrt{1 + 1} = 1.414...$

**Total GPS distance:** ≈ 11.650281 units

#### 5. Result
Percentage lost = $\frac{14.313708 - 11.650281}{14.313708} \times 100$ ≈ **18.607525%**

---

## Implementation Details

### Key Functions

#### `euclidean_distance(p1, p2)`
Calculates the Euclidean distance between two points.
- **Input:** Two points as tuples `(x, y)`
- **Output:** Distance as float
- **Formula:** $\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$

#### `interpolate_position(waypoints, target_time)`
Finds the runner's position at a specific time using linear interpolation.
- **Input:** List of waypoints `[(x, y, t), ...]`, target time
- **Output:** Interpolated position `(x, y)`
- **Method:** Linear interpolation between the two waypoints bracketing the target time

#### `calculate_total_distance(points)`
Sums the distances along a path.
- **Input:** List of points `[(x, y), ...]`
- **Output:** Total distance as float

#### `generate_gps_times(end_time, interval)`
Creates the list of GPS sampling times.
- **Input:** End time, GPS interval
- **Output:** List of sample times `[0, t, 2t, ..., end_time]`

#### `solve()`
Main solution function that orchestrates the algorithm.

---

## Complexity Analysis

### Time Complexity
- **Actual distance calculation:** O(n) where n is the number of waypoints
- **GPS sample generation:** O(T/t) where T is total time, t is GPS interval
- **Position interpolation:** O((T/t) × n) - for each GPS sample, find the right segment
- **GPS distance calculation:** O(T/t)

**Overall:** O(n × T/t)

### Space Complexity
- **Waypoint storage:** O(n)
- **GPS positions:** O(T/t)

**Overall:** O(n + T/t)

---

## Edge Cases Handled

1. **GPS interval equals total run time:** Only two samples (start and end)
2. **End time is exact multiple of t:** Avoid duplicate final timestamp
3. **Very small/large coordinates:** Use floating-point arithmetic throughout
4. **Single segment path:** Works with minimum two waypoints

---

## Testing

### Sample Input/Output

**Input:**
```
6 2
0 0 0
0 3 3
-2 5 5
0 7 7
2 5 9
0 3 11
```

**Expected Output:**
```
18.60752550117103
```

**Actual Output:**
```
18.607525501171025
```

✓ **Result:** Within required 10⁻⁵ tolerance

---

## Running the Solution

```bash
python3 imperfect_gps.py < sample_input.txt
```

Or with direct input:
```bash
python3 imperfect_gps.py
```
Then type the input and press Ctrl+D (Unix/Mac) or Ctrl+Z (Windows) to send EOF.

---

## Key Insights

1. **Linear Interpolation is Essential:** The GPS doesn't necessarily sample at waypoint times, so we must calculate intermediate positions accurately.

2. **Constant Speed Assumption:** Between any two waypoints, the runner moves at constant speed, making linear interpolation appropriate.

3. **GPS Always Records Last Position:** This is crucial - even if the run doesn't end at a multiple of t, the GPS captures the final position.

4. **Percentage vs Absolute Loss:** The problem asks for a percentage, which normalizes the result across different run lengths.

5. **Floating-Point Precision:** Using Python's built-in float (double precision) is sufficient for the 10⁻⁵ tolerance requirement.
