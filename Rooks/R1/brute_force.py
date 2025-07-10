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



with open('Rooks/R1/R1.in', 'r') as f:
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
        r, c, t = lines[line_idx].strip().split()
        rooks.append((int(r), int(c), t))
        line_idx += 1
    
    result = count_rook_moves(d, rooks)
    results.append(str(result))

with open('Rooks/R1/R1_BF.txt', 'w') as f:
    f.write('\n'.join(results) + '\n')
