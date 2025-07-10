import sys

class PRNG:
    def __init__(self, seed): self.seed = seed

    def _random(self):
        M, A = 2147483647, 16807
        Q, R = M // A, M % A
        self.seed = A * (self.seed % Q) - R * (self.seed // Q)
        if self.seed <= 0: self.seed += M
        return self.seed

    def randint(self, start, end):
        res = start + int(self._random() % (end - start + 1))
        return res

    def choice(self, seq):
        return seq[self.randint(0, len(seq) - 1)]

    def sample(self, lo, hi, count):
        answer = set()
        while len(answer) < count: answer.add( self.randint(lo, hi) )
        return sorted(list(answer))

class Checksum:
    def __init__(self): self.chk = 47

    def add(self, *xs):
        for x in xs:
            assert isinstance(x, int)
            self.chk = (42 * self.chk + x) % 123455678901

    def check(self, expected):
        if self.chk != expected:
            raise RuntimeError("Internal error, something went wrong. Expected checksum %d got %d" % (expected, self.chk) )

def count_rook_moves(d, rooks):
    MOD = 10**9 + 7
    
    board = {}
    white_rooks = []
    black_rooks = []
    
    for r, c, color in rooks:
        board[(r, c)] = color
        if color == 'W':
            white_rooks.append((r, c))
        else:
            black_rooks.append((r, c))
    
    def get_valid_moves(r, c, color, current_board):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            while 0 <= nr < d and 0 <= nc < d:
                if (nr, nc) in current_board:
                    if current_board[(nr, nc)] != color:
                        moves.append((nr, nc))
                    break
                else:
                    moves.append((nr, nc))
                    nr, nc = nr + dr, nc + dc
        
        return moves
    
    total_ways = 0
    
    for wr, wc in white_rooks:
        white_moves = get_valid_moves(wr, wc, 'W', board)
        
        for new_wr, new_wc in white_moves:
            new_board = board.copy()
            del new_board[(wr, wc)]  # Remove white rook from old position
            new_board[(new_wr, new_wc)] = 'W'  # Place white rook in new position
            
            current_black_rooks = black_rooks.copy()
            if (new_wr, new_wc) in board and board[(new_wr, new_wc)] == 'B':
                current_black_rooks.remove((new_wr, new_wc))
            
            for br, bc in current_black_rooks:
                black_moves = get_valid_moves(br, bc, 'B', new_board)
                total_ways = (total_ways + len(black_moves)) % MOD
    
    return total_ways


def count_rook_moves(d, rooks):
    """
    Count the number of ways to make one white rook move followed by one black rook move.
    
    Args:
        d: board size (d x d)
        rooks: list of (row, col, color) tuples where color is 'W' or 'B'
    
    Returns:
        Number of valid move sequences modulo 10^9 + 7
    """
    MOD = 10**9 + 7
    
    # Create board representation
    board = {}
    white_rooks = []
    black_rooks = []
    
    for r, c, color in rooks:
        board[(r, c)] = color
        if color == 'W':
            white_rooks.append((r, c))
        else:
            black_rooks.append((r, c))
    
    def get_valid_moves(r, c, color, current_board):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            while 0 <= nr < d and 0 <= nc < d:
                if (nr, nc) in current_board:
                    if current_board[(nr, nc)] != color:
                        moves.append((nr, nc))
                    break
                else:
                    moves.append((nr, nc))
                    nr, nc = nr + dr, nc + dc
        
        return moves
    
    total_ways = 0
    
    for wr, wc in white_rooks:
        white_moves = get_valid_moves(wr, wc, 'W', board)
        
        for new_wr, new_wc in white_moves:
            new_board = board.copy()
            del new_board[(wr, wc)]  
            new_board[(new_wr, new_wc)] = 'W'
            
            current_black_rooks = black_rooks.copy()
            if (new_wr, new_wc) in board and board[(new_wr, new_wc)] == 'B':
                current_black_rooks.remove((new_wr, new_wc))
            
            for br, bc in current_black_rooks:
                black_moves = get_valid_moves(br, bc, 'B', new_board)
                total_ways = (total_ways + len(black_moves)) % MOD
    
    return total_ways

CHKSUM = 36494177703
MAXD = 10**9
MAXN = 10**6

random = PRNG(4747)
chk = Checksum()

TESTS = [ (MAXD,7), (MAXD,42), (MAXN//10,MAXN), (MAXN,MAXN), (10*MAXN,MAXN) ]
TESTS += 13 * [ (MAXD,MAXN) ]
TESTS += [ (MAXD,MAXN,1,int(1.1*MAXN)), (MAXD,MAXN,int(1.1*MAXN),1), (MAXD,MAXN,2,MAXN), (MAXD,MAXN,MAXN//4,5,95) ]
TESTS += [ (MAXD,MAXN,2000,MAXN//1900), (MAXD,MAXN,2000,MAXN//1900,90) ]
TESTS += [ (MAXD,MAXN,MAXN//5,MAXN//5), (MAXD,MAXN,MAXN//5,MAXN//5,90) ]
TESTS += [ (MAXD,MAXN,MAXN//3,MAXN//3), (MAXD,MAXN,MAXN//3,MAXN//3,95) ]
TESTS += [ (MAXD,MAXN,MAXN,MAXN), (MAXD,MAXN,MAXN,MAXN,85) ]

assert len(TESTS) == 30
print(len(TESTS))

results = []

for nt, test in enumerate(TESTS):
    print(f'Generating test {nt+1}/{len(TESTS)}',file=sys.stderr)
    d, n = test[:2]
    sr, sc, gridprob = 1, 1, 0
    if len(test) >= 3: sr = test[2]
    if len(test) >= 4: sc = test[3]
    if len(test) >= 5: gridprob = test[4]

    rows = random.sample(0, d-1, sr)
    cols = random.sample(0, d-1, sc)
    rooks = []
    occupied = set()
    while len(rooks) < n:
        if random.randint(0, 99) < gridprob:
            r, c = random.choice(rows), random.choice(cols)
        else:
            r, c = random.randint(0,d-1), random.randint(0,d-1)
        if (r, c) in occupied: continue
        occupied.add((r, c))
        rooks.append((r, c, 'BW'[random.randint(0,1)]))
    print(d, n)
    for rook in rooks: 
        print(*rook)
        chk.add(rook[0], rook[1], ord(rook[2]))

    result = count_rook_moves(d, rooks)
    results.append(result)

chk.check(CHKSUM)

with open('Rooks/R3/R3_BF.txt', 'w') as f:
    f.write('\n'.join(results) + '\n')