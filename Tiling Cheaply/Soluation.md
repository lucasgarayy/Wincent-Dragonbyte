## Solution Overview

Two implementations are provided:

### 1. Basic Backtracking (`solution.py`)
A straightforward backtracking approach suitable for small grids.

### 2. Memoized Backtracking (`solution_memo.py`)
An optimized version with state memoization for handling larger grids more efficiently.

## Key Components

### Piece Representation
```python
figures = [[(0,0), (1,0), (1,1)], # L
           [(0,1), (0,2), (1,0), (1,1)], # S
           [(0,0), (0,1), (1,1), (1,2)], # Z
           [(0,0), (0,1), (1,0), (1,1)]] # O
```
Each piece is defined by coordinate offsets, with all 4 rotations pre-computed for each piece type.

## Algorithm Breakdown

### 1. Basic Backtracking Algorithm

#### Core Strategy:
- **Greedy Placement**: Always fills the first empty cell found (scanning left-to-right, top-to-bottom)
- **Cost Pruning**: Abandons branches when current cost exceeds the best known solution
- **Piece Ordering**: Processes pieces in reverse order (O, Z, S, L) to find cheaper solutions first

#### Key Functions:
```python
def backtrack(self, fig_id, current_cost):
    if current_cost >= self.best_cost:  # Pruning
        return False
    
    empty = self.next_empty()  # Find next empty cell
    if not empty:  # Board complete
        self.best_layout = [row[:] for row in self.board]
        self.best_cost = current_cost
        return True
```

### 2. Memoized Backtracking Enhancement

The memoized version adds **state caching** to avoid redundant computation:

```python
def backtrack(self, fig_id, current_cost):
    if current_cost >= self.best_cost:
        return False
    
    sig = self.board_signature()  # Create board state signature
    
    prev_cost = self.memo.get(sig)
    if prev_cost is not None and current_cost >= prev_cost:
        return False  # Skip if we've seen this state with better cost
    self.memo[sig] = current_cost
    
    # ... rest of backtracking logic
```

#### Key Improvements:
- **State Memoization**: Stores the minimum cost to reach each board configuration
- **Duplicate State Pruning**: Avoids re-exploring states that were reached with lower cost
- **Memory vs. Time Trade-off**: Uses more memory but significantly reduces computation time

## Optimization Techniques

### Both Versions:
1. **Early Termination**: Returns when first complete solution is found
2. **Cost Pruning**: Skips branches exceeding current best cost
3. **Piece Ordering**: Tries free pieces before expensive L-pieces
4. **Greedy Filling**: Always fills leftmost-topmost empty cell

### Memoized Version Only:
4. **State Caching**: Remembers minimum cost to reach each board state
5. **Redundant Path Elimination**: Avoids re-exploring equivalent states

## Solution Visualization

The `color_regions()` method converts numerical solutions to visual representations:

1. **Region Detection**: Uses BFS flood-fill to identify connected regions
2. **Graph Coloring**: Applies greedy 4-coloring algorithm to adjacent regions
3. **Output Mapping**: Maps piece types to characters (l, s, g, x)

## Performance Characteristics

### Basic Version (`solution.py`):
- **Time Complexity**: O(4^(n²)) in worst case
- **Space Complexity**: O(n²) for recursion stack
- **Suitable for**: Small grids (n ≤ 8)

### Memoized Version (`solution_memo.py`):
- **Time Complexity**: O(4^(n²)) worst case, but with significant practical speedup
- **Space Complexity**: O(4^k × n²) where k is the effective search depth
- **Suitable for**: Medium grids (n ≤ 20)

## Key Insights

1. **Cost Structure**: Only L-pieces cost 1, so the algorithm minimizes L-piece usage
2. **Deterministic Placement**: Greedy empty-cell selection ensures consistent ordering
3. **State Space Reduction**: Memoization dramatically reduces redundant computations
4. **Visual Output**: Coloring system helps visualize piece arrangements

## Missed Optimization for Large Grids (T3 Task)

For the T3 task with n ≈ 150, a crucial mathematical insight was missed during the challenge:

### The Parity Problem
- Each Tetris piece covers exactly **4 cells**
- For a complete solution, total cells (n²) must be divisible by 4
- **Odd n**: n² is always odd, making complete coverage impossible
- **Even n**: n² is divisible by 4, allowing potential solutions

### Optimal Strategy for Large n:
1. **Quick Parity Check**: `if n % 2 == 1: return "NO"`
2. **Template Padding**: For large even n, solve a smaller board and pad with a known pattern
3. **Computational Savings**: Avoid expensive backtracking for impossible cases

This mathematical pre-filtering would have saved significant computation time and immediately identified unsolvable instances.

The algorithm efficiently solves small-to-medium Tetris puzzles by combining intelligent search pruning with systematic piece placement, making it suitable for puzzle sizes where exhaustive search is feasible.