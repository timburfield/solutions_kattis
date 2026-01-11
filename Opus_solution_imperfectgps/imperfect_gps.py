"""
Imperfect GPS - Kattis Problem Solution

Calculate the percentage of running distance lost due to GPS sampling.
"""
import math


def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def interpolate_position(waypoints, target_time):
    """
    Find the runner's position at a given time using linear interpolation.
    
    Args:
        waypoints: List of (x, y, time) tuples
        target_time: The time at which to find the position
    
    Returns:
        (x, y) tuple representing the interpolated position
    """
    # Find the segment containing target_time
    for i in range(len(waypoints) - 1):
        x1, y1, t1 = waypoints[i]
        x2, y2, t2 = waypoints[i + 1]
        
        if t1 <= target_time <= t2:
            # Linear interpolation
            if t2 == t1:  # Edge case: same time (shouldn't happen per problem)
                return (x1, y1)
            
            ratio = (target_time - t1) / (t2 - t1)
            x = x1 + ratio * (x2 - x1)
            y = y1 + ratio * (y2 - y1)
            return (x, y)
    
    # Should not reach here if target_time is within bounds
    return None


def calculate_total_distance(points):
    """Calculate total distance along a path of points."""
    total = 0.0
    for i in range(len(points) - 1):
        total += euclidean_distance(points[i], points[i + 1])
    return total


def generate_gps_times(end_time, interval):
    """
    Generate GPS sample times: 0, t, 2t, ... plus end_time.
    
    Args:
        end_time: The final time of the run
        interval: GPS sampling interval
    
    Returns:
        List of sample times
    """
    times = []
    current = 0
    
    while current < end_time:
        times.append(current)
        current += interval
    
    # Always include end time (even if it's a multiple of interval, 
    # we avoid duplicates by checking)
    if not times or times[-1] != end_time:
        times.append(end_time)
    
    return times


def solve():
    """Main solution function."""
    # Read input
    first_line = input().split()
    n = int(first_line[0])
    t = int(first_line[1])
    
    waypoints = []
    for _ in range(n):
        line = input().split()
        x, y, time = int(line[0]), int(line[1]), int(line[2])
        waypoints.append((x, y, time))
    
    # Calculate actual distance
    actual_points = [(wp[0], wp[1]) for wp in waypoints]
    actual_distance = calculate_total_distance(actual_points)
    
    # Get end time
    end_time = waypoints[-1][2]
    
    # Generate GPS sample times
    gps_times = generate_gps_times(end_time, t)
    
    # Calculate GPS positions by interpolation
    gps_positions = []
    for sample_time in gps_times:
        pos = interpolate_position(waypoints, sample_time)
        gps_positions.append(pos)
    
    # Calculate GPS-measured distance
    gps_distance = calculate_total_distance(gps_positions)
    
    # Calculate percentage lost
    percentage_lost = ((actual_distance - gps_distance) / actual_distance) * 100
    
    print(percentage_lost)


if __name__ == "__main__":
    solve()
