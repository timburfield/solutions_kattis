"""
Cowboy Checkers (Nine Men's Morris) - Double Mill Detection

Board layout (7x7 grid, only 24 valid positions):
Row indices in input: 0=top (row 7), 6=bottom (row 1)
Column indices: 0=a, 1=b, ..., 6=g

Valid positions form 3 concentric squares plus 4 cross-connections.
"""

import sys

# Define valid positions on the board (row, col) in input coordinates
# Outer square
OUTER_SQUARE = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 6), (6, 0), (6, 3), (6, 6)]
# Middle square  
MIDDLE_SQUARE = [(1, 1), (1, 3), (1, 5), (3, 1), (3, 5), (5, 1), (5, 3), (5, 5)]
# Inner square
INNER_SQUARE = [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]

VALID_POSITIONS = set(OUTER_SQUARE + MIDDLE_SQUARE + INNER_SQUARE)

# Define all possible mills (sets of 3 positions that form a mill)
MILLS = [
    # Outer square - horizontal
    [(0, 0), (0, 3), (0, 6)],  # top row
    [(6, 0), (6, 3), (6, 6)],  # bottom row
    # Outer square - vertical
    [(0, 0), (3, 0), (6, 0)],  # left column
    [(0, 6), (3, 6), (6, 6)],  # right column
    
    # Middle square - horizontal
    [(1, 1), (1, 3), (1, 5)],  # top row
    [(5, 1), (5, 3), (5, 5)],  # bottom row
    # Middle square - vertical
    [(1, 1), (3, 1), (5, 1)],  # left column
    [(1, 5), (3, 5), (5, 5)],  # right column
    
    # Inner square - horizontal
    [(2, 2), (2, 3), (2, 4)],  # top row
    [(4, 2), (4, 3), (4, 4)],  # bottom row
    # Inner square - vertical
    [(2, 2), (3, 2), (4, 2)],  # left column
    [(2, 4), (3, 4), (4, 4)],  # right column
    
    # Cross connections - vertical (through middle)
    [(0, 3), (1, 3), (2, 3)],  # top vertical
    [(4, 3), (5, 3), (6, 3)],  # bottom vertical
    # Cross connections - horizontal (through middle)
    [(3, 0), (3, 1), (3, 2)],  # left horizontal
    [(3, 4), (3, 5), (3, 6)],  # right horizontal
]

# Define adjacency (which positions are connected by lines)
def build_adjacency():
    adj = {pos: [] for pos in VALID_POSITIONS}
    
    # Outer square edges
    adj[(0, 0)].extend([(0, 3), (3, 0)])
    adj[(0, 3)].extend([(0, 0), (0, 6), (1, 3)])
    adj[(0, 6)].extend([(0, 3), (3, 6)])
    adj[(3, 0)].extend([(0, 0), (6, 0), (3, 1)])
    adj[(3, 6)].extend([(0, 6), (6, 6), (3, 5)])
    adj[(6, 0)].extend([(3, 0), (6, 3)])
    adj[(6, 3)].extend([(6, 0), (6, 6), (5, 3)])
    adj[(6, 6)].extend([(6, 3), (3, 6)])
    
    # Middle square edges
    adj[(1, 1)].extend([(1, 3), (3, 1)])
    adj[(1, 3)].extend([(1, 1), (1, 5), (0, 3), (2, 3)])
    adj[(1, 5)].extend([(1, 3), (3, 5)])
    adj[(3, 1)].extend([(1, 1), (5, 1), (3, 0), (3, 2)])
    adj[(3, 5)].extend([(1, 5), (5, 5), (3, 6), (3, 4)])
    adj[(5, 1)].extend([(3, 1), (5, 3)])
    adj[(5, 3)].extend([(5, 1), (5, 5), (6, 3), (4, 3)])
    adj[(5, 5)].extend([(5, 3), (3, 5)])
    
    # Inner square edges
    adj[(2, 2)].extend([(2, 3), (3, 2)])
    adj[(2, 3)].extend([(2, 2), (2, 4), (1, 3)])
    adj[(2, 4)].extend([(2, 3), (3, 4)])
    adj[(3, 2)].extend([(2, 2), (4, 2), (3, 1)])
    adj[(3, 4)].extend([(2, 4), (4, 4), (3, 5)])
    adj[(4, 2)].extend([(3, 2), (4, 3)])
    adj[(4, 3)].extend([(4, 2), (4, 4), (5, 3)])
    adj[(4, 4)].extend([(4, 3), (3, 4)])
    
    return adj

ADJACENCY = build_adjacency()

def parse_board(lines):
    """Parse input and return set of White positions and set of Black positions."""
    white = set()
    black = set()
    
    for row in range(7):
        for col in range(7):
            if (row, col) in VALID_POSITIONS:
                char = lines[row][col]
                if char == 'W':
                    white.add((row, col))
                elif char == 'B':
                    black.add((row, col))
    
    return white, black

def get_mills_for_position(pos):
    """Return list of mills that contain the given position."""
    return [mill for mill in MILLS if pos in mill]

def is_complete_mill(mill, white_positions):
    """Check if all 3 positions in the mill are occupied by White."""
    return all(pos in white_positions for pos in mill)

def has_double_mill(white_positions, black_positions):
    """
    Check if White has a double mill.
    
    A double mill exists when:
    1. White has a complete mill
    2. One piece from that mill can move to an adjacent empty position
    3. That move completes another mill
    4. The original mill now has 2 white pieces (can be closed again)
    """
    occupied = white_positions | black_positions
    
    # Find all complete mills for White
    complete_mills = [mill for mill in MILLS if is_complete_mill(mill, white_positions)]
    
    for mill in complete_mills:
        # Try moving each piece in this mill
        for piece in mill:
            # Check each adjacent position
            for neighbor in ADJACENCY[piece]:
                if neighbor not in occupied:  # Can move here
                    # Simulate the move
                    new_white = white_positions - {piece} | {neighbor}
                    
                    # Check if this creates a new complete mill (not the original one)
                    for other_mill in MILLS:
                        if other_mill == mill:
                            continue
                        if neighbor in other_mill and is_complete_mill(other_mill, new_white):
                            # Found a double mill!
                            # The original mill now has 2 pieces, new mill has 3
                            return True
    
    return False

def main():
    lines = []
    for _ in range(7):
        line = input()
        # Ensure line is exactly 7 characters
        line = line.ljust(7)
        lines.append(line)
    
    white, black = parse_board(lines)
    
    if has_double_mill(white, black):
        print("double mill")
    else:
        print("no double mill")

if __name__ == "__main__":
    main()
