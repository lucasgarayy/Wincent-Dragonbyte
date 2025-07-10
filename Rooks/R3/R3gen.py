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

chk.check(CHKSUM)
