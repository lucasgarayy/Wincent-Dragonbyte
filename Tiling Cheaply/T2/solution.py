from collections import deque, defaultdict
import time

start_time = time.time()

class Piece:
    # Working in y, x not x, y 
    figures = [[(0,0), (1,0), (1,1)], # L
               [(0,1), (0,2), (1,0), (1,1)], # S
               [(0,0), (0,1), (1,1), (1,2)], # Z
               [(0,0), (0,1), (1,0), (1,1)]] # O
    
    # Figure Id 0 -> L, 1 -> S, 2 -> Z, 3 -> O 
    def __init__(self, fig_id):
        self.fig_id = fig_id
        self.figure = self.figures[fig_id]
        self.cost = 1 if fig_id == 0 else 0
        self.possible_pos = [self.figure]
        for _ in range(3):  
            new_rotation = self.normalize(self.rotate_90(self.possible_pos[-1]))
            self.possible_pos.append(new_rotation)
    
    def normalize(self, figure):
        min_x = min(x for x, y in figure)
        min_y = min(y for x, y in figure)
        return [(x - min_x, y - min_y) for x, y in figure]
    
    def rotate_90(self, figure):
        return [(-x, y) for (y, x) in figure]
    

class Puzzle:
    def __init__(self, n):
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.best_cost = 9999
        self.best_layout = None
        self.figures = [Piece(i) for i in range(4)][::-1]
    
    def can_place(self, fig_pos, pos):
        y, x = pos
        for (f_y, f_x) in fig_pos:
            new_y, new_x = y + f_y, x + f_x
            if not (0 <= new_y < self.n and 0 <= new_x < self.n):
                return False
            if self.board[new_y][new_x] != 0:
                return False
        return True

    
    def place(self, fig_pos, fig_id, pos):
        y, x = pos
        for (f_y, f_x) in fig_pos:
            self.board[y+f_y][x+f_x] = fig_id

    def is_solved(self):
        return all(all(cell != 0 for cell in row) for row in self.board)
    
    def next_empty(self):
        for y in range(self.n):
            for x in range(self.n):
                if self.board[y][x] == 0:
                    return y, x
        return False


    def solve(self):
        self.backtrack(fig_id = 1, current_cost = 0)
        return self.best_layout, self.best_cost
    
    def backtrack(self, fig_id, current_cost):
        if current_cost >= self.best_cost:
            return False
        empty = self.next_empty()
        if not empty:
            self.best_layout = [row[:] for row in self.board]
            self.best_cost = current_cost
            return True
        y0, x0 = empty
        for figure in self.figures:
            for pos in figure.possible_pos:
                if not self.can_place(pos, (y0, x0)):
                    continue
                self.place(pos, fig_id, (y0, x0))
                stop = self.backtrack(fig_id + 1, current_cost + figure.cost)
                if stop:
                    return True
                self.place(pos, 0, (y0, x0))
        return False
    
    def print_board(self):
        for row in self.best_layout:
            print(f'{row}' + '\n')
     
    def color_regions(self, mat):
        R, C = len(mat), len(mat[0])
        region_id = [[None]*C for _ in range(R)]
        regions = {}  
        next_id = 0

        for i in range(R):
            for j in range(C):
                if region_id[i][j] is None:
                    val = mat[i][j]
                    # BFS flood-fill
                    q = deque([(i,j)])
                    region_id[i][j] = next_id
                    cells = [(i,j)]
                    while q:
                        x,y = q.popleft()
                        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                            nx,ny = x+dx, y+dy
                            if 0 <= nx < R and 0 <= ny < C:
                                if region_id[nx][ny] is None and mat[nx][ny] == val:
                                    region_id[nx][ny] = next_id
                                    cells.append((nx,ny))
                                    q.append((nx,ny))
                    regions[next_id] = {'value': val, 'cells': cells}
                    next_id += 1

        # 2) Build adjacency graph between regions
        adj = defaultdict(set)
        for rid, info in regions.items():
            for (x,y) in info['cells']:
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny = x+dx, y+dy
                    if 0 <= nx < R and 0 <= ny < C:
                        nbr_rid = region_id[nx][ny]
                        if nbr_rid != rid:
                            adj[rid].add(nbr_rid)
                            adj[nbr_rid].add(rid)

        colors = ['l','s','g','x']
        region_color = {}
        order = sorted(regions.keys(), key=lambda r: len(adj[r]), reverse=True)
        for rid in order:
            used = { region_color[nbr] for nbr in adj[rid] if nbr in region_color }
            for col in colors:
                if col not in used:
                    region_color[rid] = col
                    break
            else:
                raise ValueError(f"Ran out of colors for region {rid}!")  
        color_mat = [[region_color[region_id[i][j]] for j in range(C)] for i in range(R)]
        s = '\n'.join(''.join(row) for row in color_mat)
        return s

    def get_solution(self):
        
        matrix, cost = self.solve()
        if matrix:
            string = 'YES' + '\n' + self.color_regions(matrix) + '\n'
        else:
            string = 'NO' + '\n'
        return string


with open('Tiling Cheaply/T2/T2.in', 'r') as infile, \
     open('Tiling Cheaply/T2/T2_SOL.txt', 'w') as outfile:
    next(infile)
    for line in infile:
        number = int(line.strip())
        string = Puzzle(number).get_solution()
        outfile.write(f'{string}')

end_time = time.time()
print(f'Time taken{end_time - start_time}')