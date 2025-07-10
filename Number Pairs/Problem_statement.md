# Number Pairs
### Statement
All numbers in this task are non-negative integers.

When refering to their digits, we are using their standard base-10 representations.

Given a number $d$ . Find any two numbers with a difference $d$ and the same digit sum, or report that no such pair of numbers exists.

### Input format
The first line of the input file contains the number $t$ of test cases. The specified number of test cases follows, one after another.

Each test case consists of a single line containing a single number $d$.

### Output format
For each test case output a single line containing either a pair of space-separated numbers $x$ and $y$ with the desired properties, or the word “NONE” (quotes for clarity) if there is no solution.

The numbers in your output may have up to 50 digits. (It is guaranteed that if a solution exists, there is one that fits into this limit comfortably.)

### Subproblem N1 (16 Points)
Input file N1.in
Constraints:
- $t \leq 200$
- in each test case, $1 \leq d \leq 1000$
- No test case with the answer “NONE”

### Subproblem N2 (32 Points)
Input file N2.in
Constraints:
- $t \leq 200$
- in each test case, $1 \leq d \leq 10^6$


### Subproblem N3 (52 Points)
Input file N3.in
Constraints:
- $t \leq 200$
- in each test case, $1 \leq d \leq 10^{18}$
