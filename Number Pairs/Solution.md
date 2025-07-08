## Solution Overview

There are 2 solutions attempted, for N1 as the number difference `d` maximum value is 1000 the shown is just a brute force solution. A number `a` starts from 1 up to 10000 and `b` is just `a + d`. `a` and `b` digit sums are compared until a pair with same digit sum is found.


The solution for N2 and N3 are the same and uses **dynamic programming with memoization** to construct two numbers digit by digit, ensuring they maintain the required difference while having equal digit sums.

### Key Insights

1. **Digit Sum Preservation**: For two numbers to have the same digit sum when their difference is `d`, the digit sum of `d` must be divisible by 9. This is because `digit_sum(b) - digit_sum(a) ≡ b - a ≡ d (mod 9)`.

2. **Digit-by-Digit Construction**: We can build numbers `a` and `b` simultaneously by processing digits from least significant to most significant, maintaining:
   - The difference constraint: `b - a = d`
   - The digit sum constraint: `digit_sum(a) = digit_sum(b)`

## Algorithm Breakdown

### 1. Initial Validation
```python
if d == 0:
    return 0, 0  # Trivial case: both numbers are the same

if d % 9 != 0:
    return None  # Impossible case: digit sums can't be equal
```

### 2. Setup
```python
digits = list(map(int, str(d)[::-1])) + [0]  # Reverse d's digits, add padding
L = len(digits)
max_delta = 9 * L  # Maximum possible difference in digit sums
```

### 3. Dynamic Programming State
The DP function `dfs(pos, carry, delta)` represents:
- `pos`: Current digit position (0 = least significant)
- `carry`: Carry from previous digit addition
- `delta`: Current difference in digit sums (`sum(a_digits) - sum(b_digits)`)

### 4. Core Logic
For each position, we:
1. Try all possible digits `a_i` for number `a`
2. Calculate the corresponding digit `b_i` for number `b`:
   ```python
   s = a_i + d_i + carry  # Sum including carry
   b_i = s % 10           # Digit for b
   new_carry = s // 10    # Carry for next position
   ```
3. Update the digit sum difference:
   ```python
   new_delta = delta + (a_i - b_i)
   ```
4. Prune impossible branches (when `|new_delta| > max_delta`)
5. Recursively solve for the next position

### 5. Base Case
```python
if pos == L:
    return [] if (carry == 0 and delta == 0) else None
```
Success when we've processed all digits with no remaining carry and balanced digit sums.

### 6. Result Construction
Convert the digit array back to the actual number `a`, then compute `b = a + d`.
