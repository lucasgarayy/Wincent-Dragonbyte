## Solution Overview

Similarly to the other problems, I started with a brute force solution and then try to find a more optimised solution:

### 1. Brute Force Simulation (`brute_force.py`)
A straightforward approach that explicitly simulates each move sequence.

### 2. Optimized Counting (`optimised_counting.py`)
An efficient algorithm using sorted data structures and mathematical counting.

**Note**: The optimized counting implementation returns erroneous solutions. I ran out of time during the challenge, the implementation was not completed correctly, but the algorithmic approach is sound and explained below.

## Algorithm Breakdown

### 1. Brute Force Approach

#### Core Strategy:
```python
def get_valid_moves(r, c, color, current_board):
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        while 0 <= nr < d and 0 <= nc < d:
            if (nr, nc) in current_board:
                if current_board[(nr, nc)] != color:
                    moves.append((nr, nc))  # Capture
                break
            else:
                moves.append((nr, nc))  # Empty square
                nr, nc = nr + dr, nc + dc
    return moves
```

#### Process:
1. **For each white rook**: Generate all possible moves
2. **For each white move**: 
   - Simulate the move (update board state)
   - Handle captures (remove captured black rook)
   - Count all possible black rook moves in new position
3. **Accumulate**: Sum all black move counts

#### Performance Characteristics:
- **Time Complexity**: O(W × M_w × B × M_b) where:
  - W = number of white rooks
  - M_w = average moves per white rook
  - B = number of black rooks  
  - M_b = average moves per black rook
- **Space Complexity**: O(N) for board representation
- **Bottleneck**: Recalculating moves for each black rook after every white move

### 2. Optimized Counting Approach (Buggy Implementation)

#### Key Innovation:
Instead of simulating individual moves, use **sorted data structures** to efficiently count moves mathematically.

#### Data Structure Setup:
```python
# Maps of occupied columns per row and occupied rows per column
row_map = {r: [] for r in range(d)}  # row -> sorted list of occupied columns
col_map = {c: [] for c in range(d)}  # col -> sorted list of occupied rows

for r, c, color in rooks:
    insort(row_map[r], c)  # Keep sorted
    insort(col_map[c], r)  # Keep sorted
```

#### Efficient Move Counting:
```python
def moves_from(r, c):
    """Return total legal moves + attack moves for a rook at (r,c)."""
    # Horizontal moves
    cols = row_map[r]
    i = bisect_left(cols, c)
    left = cols[i-1] if i > 0 else -1
    right = cols[i+1] if i+1 < len(cols) else d
    horiz_empty = (c - left - 1) + (right - c - 1)
    horiz_attacks = int(left != -1) + int(right != d)

    # Vertical moves  
    rows = col_map[c]
    j = bisect_left(rows, r)
    down = rows[j-1] if j > 0 else -1
    up = rows[j+1] if j+1 < len(rows) else d
    vert_empty = (r - down - 1) + (up - r - 1)
    vert_attacks = int(down != -1) + int(up != d)

    return horiz_empty + horiz_attacks + vert_empty + vert_attacks
```

#### Core Algorithm:
1. **Pre-compute**: Build sorted row/column occupation maps
2. **For each white rook**: Use binary search to find valid target positions
3. **For each target**: 
   - Update data structures (O(log N) per operation)
   - Count black moves using mathematical formula (O(log N) per black rook)
   - Restore data structures
4. **Accumulate**: Sum all counts

## Performance Comparison

### Brute Force (`brute_force.py`):
- **Time Complexity**: O(W × d² × B × d²) = O(W × B × d⁴)
- **Space Complexity**: O(N)
- **Move Generation**: O(d) per rook per direction
- **Board Updates**: O(1) dictionary operations
- **Bottleneck**: Redundant move calculations

### Optimized (`optimised_counting.py`):
- **Time Complexity**: O(W × M_w × B × log N) where M_w ≈ O(d)
- **Space Complexity**: O(N + d²) for sorted structures
- **Move Counting**: O(log N) per rook using binary search
- **Board Updates**: O(log N) for sorted list maintenance
- **Advantage**: Mathematical counting vs. explicit enumeration

## Key Optimizations

### 1. Sorted Data Structures
```python
from bisect import bisect_left, insort

row_map = {r: [] for r in range(d)}  # Sorted lists
col_map = {c: [] for c in range(d)}  # Sorted lists
```
- **Binary Search**: O(log N) lookups for obstacle positions
- **Efficient Updates**: O(log N) insertions/deletions
- **Range Queries**: Immediate access to blocking pieces

### 2. Mathematical Move Counting
Instead of generating each move explicitly:
```python
# Count empty squares between obstacles
empty_moves = (target_pos - last_obstacle - 1)
# Count possible captures
capture_moves = int(obstacle_exists)
```

### 3. Efficient State Management
```python
# Remove piece
idx = bisect_left(row_map[r], c)
row_map[r].pop(idx)

# Add piece  
insort(row_map[r], c)
```

## Algorithm Complexity Analysis

### Brute Force Bottlenecks:
1. **Move Generation**: O(d) per rook × 4 directions = O(d) per rook
2. **Board Simulation**: Creates new board state for each white move
3. **Redundant Calculations**: Recalculates black moves from scratch

### Optimized Advantages:
1. **Binary Search**: O(log N) vs O(d) for finding obstacles
2. **Mathematical Counting**: O(1) arithmetic vs O(d) enumeration
3. **Incremental Updates**: O(log N) state changes vs O(N) board copying

The optimized solution represents a correct algorithmic approach that would transform an O(W × B × d⁴) brute force algorithm into an O(W × B × d × log N) mathematical counting algorithm, providing orders of magnitude speedup for larger problem instances. However, due to implementation bugs, only the brute force solution produces correct results.