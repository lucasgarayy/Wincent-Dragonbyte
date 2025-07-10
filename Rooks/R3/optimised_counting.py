from bisect import bisect_left, insort
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
    """
    Efficient O((W_moves) * B * log N) exact count using sorted row/col lists.
    """
    MOD = 10**9 + 7
    whites = []
    blacks = []
    # Maps of occupied columns per row and occupied rows per column
    row_map = {r: [] for r in range(d)}
    col_map = {c: [] for c in range(d)}

    # Populate maps and color lists
    for r, c, color in rooks:
        insort(row_map[r], c)
        insort(col_map[c], r)
        if color == 'W':
            whites.append((r, c))
        else:
            blacks.append((r, c))

    def moves_from(r, c):
        """Return total legal moves + attack moves for a rook at (r,c)."""
        # Horizontal
        cols = row_map[r]
        i = bisect_left(cols, c)
        left = cols[i-1] if i > 0 else -1
        right = cols[i+1] if i+1 < len(cols) else d
        horiz_empty = (c - left - 1) + (right - c - 1)
        horiz_attacks = int(left != -1) + int(right != d)

        # Vertical
        rows = col_map[c]
        j = bisect_left(rows, r)
        down = rows[j-1] if j > 0 else -1
        up = rows[j+1] if j+1 < len(rows) else d
        vert_empty = (r - down - 1) + (up - r - 1)
        vert_attacks = int(down != -1) + int(up != d)

        return horiz_empty + horiz_attacks + vert_empty + vert_attacks

    total = 0

    for wr, wc in whites:
        # Determine all legal target positions for this white rook
        cols = row_map[wr]
        i0 = bisect_left(cols, wc)
        left_bound = cols[i0-1] if i0 > 0 else -1
        right_bound = cols[i0+1] if i0+1 < len(cols) else d

        targets = []
        # Move/attack left
        for c in range(wc-1, left_bound, -1):
            targets.append((wr, c))
        if left_bound != -1:
            targets.append((wr, left_bound))
        # Move/attack right
        for c in range(wc+1, right_bound):
            targets.append((wr, c))
        if right_bound != d:
            targets.append((wr, right_bound))

        # Move/attack down
        rows = col_map[wc]
        j0 = bisect_left(rows, wr)
        down_bound = rows[j0-1] if j0 > 0 else -1
        up_bound = rows[j0+1] if j0+1 < len(rows) else d

        for r in range(wr-1, down_bound, -1):
            targets.append((r, wc))
        if down_bound != -1:
            targets.append((down_bound, wc))
        # Move/attack up
        for r in range(wr+1, up_bound):
            targets.append((r, wc))
        if up_bound != d:
            targets.append((up_bound, wc))

        # Remove original white rook
        idx = bisect_left(row_map[wr], wc)
        row_map[wr].pop(idx)
        idx = bisect_left(col_map[wc], wr)
        col_map[wc].pop(idx)

        for tr, tc in targets:
            # Check capture
            captured = (tr, tc) in blacks
            if captured:
                # Remove captured black
                bi = bisect_left(row_map[tr], tc)
                row_map[tr].pop(bi)
                bi = bisect_left(col_map[tc], tr)
                col_map[tc].pop(bi)

            # Add moved white
            insort(row_map[tr], tc)
            insort(col_map[tc], tr)

            # Sum black moves in this new position
            for br, bc in blacks:
                if captured and (br, bc) == (tr, tc):
                    continue
                total = (total + moves_from(br, bc)) % MOD

            # Undo white move
            wi = bisect_left(row_map[tr], tc)
            row_map[tr].pop(wi)
            wi = bisect_left(col_map[tc], tr)
            col_map[tc].pop(wi)

            if captured:
                # Restore captured black
                insort(row_map[tr], tc)
                insort(col_map[tc], tr)

        # Restore original white
        insort(row_map[wr], wc)
        insort(col_map[wc], wr)

    return total % MOD



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

with open('Rooks/R3/R3_SOL.txt', 'w') as f:
    f.write('\n'.join(results) + '\n')