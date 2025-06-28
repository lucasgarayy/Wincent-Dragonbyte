import heapq

class Ball:
    def __init__(self, weight, pos):
        self.weight = weight
        self.pos = pos

    def can_eat(self, w_i):
        return 2 * self.weight > w_i

    def eat(self, w_i):
        if self.can_eat(w_i):
            self.weight += w_i
            return True 
        return False
    
class State:
    def __init__(self, pos, weight, eaten, time):
        self.pos = pos
        self.weight = weight
        self.eaten = frozenset(eaten)
        self.time = time
    
    def __hash__(self):
        return hash((self.pos, self.weight, self.eaten))
    
    def __eq__(self, other):
        return (self.pos == other.pos and 
                self.weight == other.weight and 
                self.eaten == other.eaten)

    def __lt__(self, other):
        return self.time < other.time
        
def manhattan_distance(pos_a, pos_b):
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

class Puzzle:
    def __init__(self, objects_params, w_0):
        self.objects = [(x, y, w) for x, y, w in objects_params]
        self.initial_weight = w_0
        self.n_objects = len(self.objects)
    
    def get_eatable_objects(self, weight, eaten):
        eatable = []
        for i, (x, y, w) in enumerate(self.objects):
            if i not in eaten and  weight > 2 * w:
                eatable.append(i)
        return eatable
    
    def heuristic(self, state):
        eatable = self.get_eatable_objects(state.weight, state.eaten)
        if not eatable:
            return 0
        min_dist = float('inf')
        for obj_idx in eatable:
            x, y, w = self.objects[obj_idx]
            dist = manhattan_distance(state.pos, (x, y))
            min_dist = min(min_dist, dist + 1)
        return min_dist
    
    def get_max_possible_weight(self, current_weight, eaten):
        max_weight = current_weight
        remaining_objects = []
        for i, (x, y, w) in enumerate(self.objects):
            if i not in eaten:
                remaining_objects.append((w, i))
        remaining_objects.sort()
        for obj_weight, obj_idx in remaining_objects:
            if max_weight > 2 * obj_weight:
                max_weight += obj_weight
        return max_weight
    
    def solve(self):
        initial_state = State((0, 0), self.initial_weight, frozenset(), 0)
        pq = [(0, initial_state, [])]
        visited = {}
        
        best_weight = self.initial_weight
        best_solution = []
        best_time = float('inf')
        
        while pq:
            f_score, current_state, path = heapq.heappop(pq)
            
            # Use frozenset for eaten objects to make it hashable
            state_key = (current_state.pos, current_state.weight, current_state.eaten)
            
            # Skip if we've seen this state with better or equal time
            if state_key in visited and visited[state_key] <= current_state.time:
                continue
            visited[state_key] = current_state.time
            
            # Update best solution if we found better weight or same weight with less time
            if (current_state.weight > best_weight or 
                (current_state.weight == best_weight and current_state.time < best_time)):
                best_weight = current_state.weight
                best_solution = path
                best_time = current_state.time
            
            # Get eatable objects only once
            eatable = self.get_eatable_objects(current_state.weight, current_state.eaten)
            if not eatable:
                continue
            
            # Process each eatable object
            for obj_idx in eatable:
                x, y, w = self.objects[obj_idx]
                travel_time = manhattan_distance(current_state.pos, (x, y))
                total_time = current_state.time + travel_time + 1  # +1 for eat_time
                
                # Early termination: skip if this path can't improve best solution
                new_weight = current_state.weight + w
                if new_weight < best_weight and total_time >= best_time:
                    continue
                
                new_eaten = current_state.eaten | {obj_idx}
                new_state = State((x, y), new_weight, new_eaten, total_time)
                
                # Only add to queue if we haven't seen this state or found a better path
                next_state_key = (new_state.pos, new_state.weight, new_state.eaten)
                if next_state_key not in visited or visited[next_state_key] > total_time:
                    h_score = self.heuristic(new_state)
                    f_score = total_time + h_score
                    new_path = path + [obj_idx]
                    heapq.heappush(pq, (f_score, new_state, new_path))
        
        return best_solution

    
    def solve_fast_greedy(self):
        """Multi-step lookahead approach: considers 3 steps ahead for much better decision making."""
        current_pos = (0, 0)
        current_weight = self.initial_weight
        eaten = set()
        path = []
        total_time = 0
        
        while True:
            eatable = self.get_eatable_objects(current_weight, eaten)
            if not eatable:
                break
                
            # Less greedy approach: consider multiple good candidates
            candidates = []
            
            for obj_idx in eatable:
                x, y, w = self.objects[obj_idx]
                distance = manhattan_distance(current_pos, (x, y))
                time_cost = distance + 1
                score = w / time_cost
                candidates.append((obj_idx, score, distance, w))
            
            # Sort by score descending
            candidates.sort(key=lambda x: x[1], reverse=True)
            
            # Consider top 3 candidates (or fewer if not available)
            top_candidates = candidates[:min(3, len(candidates))]
            
            best_obj = None
            best_future_score = -1
            
            # Multi-step lookahead for each top candidate
            for obj_idx, current_score, distance, weight in top_candidates:
                x, y, w = self.objects[obj_idx]
                
                # Calculate lookahead score with multiple steps
                lookahead_score = self._calculate_lookahead_score(
                    pos=(x, y),
                    weight=current_weight + w,
                    eaten=eaten | {obj_idx},
                    depth=3,  # Look 3 steps ahead
                    discount_factor=0.7
                )
                
                # Combined score: current benefit + discounted future potential
                combined_score = current_score + lookahead_score
                
                if combined_score > best_future_score:
                    best_future_score = combined_score
                    best_obj = obj_idx
            
            if best_obj is None:  # This should not happen if eatable is not empty
                break
                
            # Move to and eat the best object
            x, y, w = self.objects[best_obj]
            travel_time = manhattan_distance(current_pos, (x, y))
            total_time += travel_time + 1  # +1 for eating time
            
            current_pos = (x, y)
            current_weight += w
            eaten.add(best_obj)
            path.append(best_obj)
        return path 

        
    def _calculate_lookahead_score(self, pos, weight, eaten, depth, discount_factor):
        """Recursively calculate the best possible score from this state with given depth."""
        if depth <= 0:
            return 0
        
        eatable = self.get_eatable_objects(weight, eaten)
        if not eatable:
            return 0
        
        # Find top candidates at this level
        candidates = []
        for obj_idx in eatable:
            x, y, w = self.objects[obj_idx]
            distance = manhattan_distance(pos, (x, y))
            time_cost = distance + 1
            score = w / time_cost
            candidates.append((obj_idx, score, x, y, w))
        
        # Sort and take top candidates (fewer at deeper levels to control complexity)
        max_candidates = max(1, 4 - depth)  # 3 candidates at depth 1, 2 at depth 2, 1 at depth 3
        candidates.sort(key=lambda x: x[1], reverse=True)
        top_candidates = candidates[:max_candidates]
        
        best_future_score = 0
        
        # For each candidate, calculate immediate score + recursive lookahead
        for obj_idx, immediate_score, x, y, w in top_candidates:
            # Recursive lookahead from this position
            future_score = self._calculate_lookahead_score(
                pos=(x, y),
                weight=weight + w,
                eaten=eaten | {obj_idx},
                depth=depth - 1,
                discount_factor=discount_factor
            )
            
            # Combine immediate and future scores with discount
            total_score = immediate_score + discount_factor * future_score
            best_future_score = max(best_future_score, total_score)
        
        return best_future_score



def solver_wrapper(in_path, out_path):
    with open(in_path, 'r') as f, open(out_path, 'w') as fout:
        it = iter(map(int, f.read().split()))
        T = next(it)
        for _ in range(T):
            n, W = next(it), next(it)
            items = [(next(it), next(it), next(it)) for _ in range(n)]
            puzzle = Puzzle(items, W)
            solution = puzzle.solve_fast_greedy()
            fout.write(f'{len(solution)}\n')
            fout.write(' '.join(map(str, solution)) + '\n')
            print('Solved')

solver_wrapper('Katamari/K1.in', 'Katamari/K1_greedy.txt')