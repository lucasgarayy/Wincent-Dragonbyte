# Rooks
### Statement
We have a $d x d$ chessboard. Both rows and columns of the board are numbered from $0$ to $d-1$.

On the board are $n$ rooks – some white, others black. For each rook you are given its row $r_i$, its column $c_i$ and its type $t_i$: either ‘W’ or ‘B’.

You want to make one valid move with a white rook, followed by one valid move with a black rook. Count the ways in which this can be done.

### Rook moves

A rook moves horizontally or vertically, through any number of unoccupied squares. It may end its move either on an unoccupied square, or on a square occupied by a piece of the opposite color. In the latter case, the opposite-color piece is captured and removed from the board.

The rook must actually move – its destination square must be different from its starting square.

### Input format
The first line of each input file contains the number 
 of test cases. The specified number of test cases follows, one after another.

Each test case consists of one or more lines.

- Line 1: the numbers $d$ and $n$.
- Lines 2 to $n+1$: numbers $r_i$ and $c_i$ and letter $t_i$ describing one of the rooks.

All rooks are guaranteed to be on mutually distinct squares of the chessboard.

Output format
For each test case, output a single line with a single integer: the desired number of ways, modulo $10^9 + 7$.