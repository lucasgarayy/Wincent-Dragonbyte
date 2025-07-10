from bisect import bisect_left, insort

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


def solve_from_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    results = []
    line_idx = 0
    
    t = int(lines[line_idx].strip())
    line_idx += 1
    
    for _ in range(t):
        d, n = map(int, lines[line_idx].strip().split())
        line_idx += 1
        
        rooks = []
        for _ in range(n):
            r, c, color = lines[line_idx].strip().split()
            rooks.append((int(r), int(c), color))
            line_idx += 1
        
        result = count_rook_moves(d, rooks) 
        results.append(str(result))
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(results) + '\n')

solve_from_file('Rooks/R2/R2.in', 'Rooks/R2/R2_SOL.txt')