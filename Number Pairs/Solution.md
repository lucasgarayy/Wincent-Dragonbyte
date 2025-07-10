## Solution Overview

Two implementations are provided with vastly different approaches and performance characteristics:

### 1. Brute Force (`brute_force.py`)
A simple iterative approach that tests numbers sequentially.

### 2. Dynamic Programming (`digit_dp.py`)
An optimized digit-by-digit construction using memoized recursion.

## Algorithm Breakdown

### 1. Brute Force Approach

#### Core Strategy:
```python
def find_pair(d):
    for a in range(1, 1000000):
        b = d + a
        if sum_digits(a) == sum_digits(b):
            return a, b
    return None
```

- **Linear Search**: Tests values of `a` from 1 to 1,000,000
- **Direct Computation**: For each `a`, computes `b = a + d`
- **Digit Sum Comparison**: Checks if `sum_digits(a) == sum_digits(b)`
- **First Match**: Returns the first valid pair found

#### Performance Characteristics:
- **Time Complexity**: O(n) where n is the search limit (1,000,000)
- **Space Complexity**: O(1)
- **Suitable for**: Small differences where solutions exist early
- **Limitation**: Fixed search bound may miss solutions

### 2. Dynamic Programming Approach

#### Mathematical Foundation:
The key insight is that for two numbers to have equal digit sums when their difference is `d`:
```
digit_sum(b) - digit_sum(a) ≡ b - a ≡ d (mod 9)
```

Therefore, if `d % 9 ≠ 0`, no solution exists.

#### Core Strategy:
```python
def find_pair_digit_dp(d):
    if d == 0:
        return 0, 0
    
    if d % 9 != 0:
        return None  # Impossible case
    
    # Build numbers digit by digit
    digits = list(map(int, str(d)[::-1])) + [0]
    L = len(digits)
    max_delta = 9 * L
```

#### State Space Definition:
The DP function `dfs(pos, carry, delta)` represents:
- `pos`: Current digit position (0 = least significant)
- `carry`: Carry from previous digit addition
- `delta`: Current difference in digit sums (`sum(a_digits) - sum(b_digits)`)

#### Digit Construction Logic:
```python
for a_i in range(10):
    s = a_i + d_i + carry
    b_i = s % 10
    new_carry = s // 10
    
    new_delta = delta + (a_i - b_i)
    if abs(new_delta) > max_delta:
        continue  # Pruning impossible branches
    
    res = dfs(pos + 1, new_carry, new_delta)
    if res is not None:
        return [a_i] + res
```

#### Key Optimizations:
1. **Early Termination**: Returns immediately when `d % 9 ≠ 0`
2. **Memoization**: Uses `@lru_cache(None)` to avoid recomputing states
3. **Pruning**: Skips branches where `|delta| > max_delta`
4. **Digit-by-Digit**: Constructs minimal solutions systematically

## Performance Comparison

### Brute Force (`brute_force.py`):
- **Time Complexity**: O(n) where n ≤ 1,000,000
- **Space Complexity**: O(1)
- **Strengths**: Simple, guaranteed to find small solutions
- **Weaknesses**: Limited search range, inefficient for large differences

### Dynamic Programming (`solution.py`):
- **Time Complexity**: O(10 × L × C × D) where L = digits in d, C = carry states, D = delta states
- **Space Complexity**: O(L × C × D) for memoization
- **Strengths**: Finds minimal solutions, handles large differences, mathematically complete
- **Weaknesses**: More complex implementation, higher memory usage

## Key Insights

### 1. Mathematical Constraint
```python
if d % 9 != 0:
    return None  # No solution exists
```
This eliminates impossible cases immediately, saving computation time.

### 2. Digit Sum Preservation
For any two numbers `a` and `b`:
- `digit_sum(a) ≡ a (mod 9)`
- `digit_sum(b) ≡ b (mod 9)`
- Therefore: `digit_sum(b) - digit_sum(a) ≡ b - a ≡ d (mod 9)`

### 3. Minimal Solution Construction
The DP approach constructs the lexicographically smallest solution by:
- Processing digits from least to most significant
- Trying digit values 0-9 in order
- Using memoization to avoid redundant computations

## Algorithm Breakdown Detail

### Brute Force Process:
1. **Iterate**: `a` from 1 to 1,000,000
2. **Calculate**: `b = a + d`
3. **Check**: `sum_digits(a) == sum_digits(b)`
4. **Return**: First valid pair or None

### DP Process:
1. **Validate**: Check if `d % 9 == 0`
2. **Setup**: Reverse digits of `d`, add padding
3. **Recursion**: Build digits maintaining constraints
4. **Memoization**: Cache results for (position, carry, delta)
5. **Construct**: Convert digit array back to number

## Performance Characteristics

### Small Differences (d < 1000):
- **Brute Force**: Fast, finds solutions quickly
- **DP**: Overhead may be higher, but guaranteed minimal solution

### Large Differences (d > 1000):
- **Brute Force**: May fail if solution > 1,000,000
- **DP**: Efficiently constructs minimal solutions regardless of size

### Impossible Cases:
- **Brute Force**: Searches entire range before failing
- **DP**: Immediately returns None after modulo check

The DP solution is mathematically complete and efficient for all valid inputs, while the brute force approach provides a simple alternative for small cases with the risk of missing solutions beyond its search limit.