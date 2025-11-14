Import heapq

# Goal state for 8 puzzle
GOAL_STATE = ((1, 2, 3),
              (8, 0, 4),
              (7, 6, 5))

# Moves - up, down, left, right
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan_distance(state):
    """Calculate the total Manhattan distance of the current state to the goal."""
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_x, goal_y = divmod(value - 1, 3)
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

def get_neighbors(state):
    """Generate neighbors by sliding the blank tile (0) in all possible directions."""
    neighbors = []
    # Find the blank (zero) position
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = i, j
                break
   
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            # Swap blank with adjacent tile to generate a new state
            new_state = [list(row) for row in state]  # deep copy
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(tuple(tuple(row) for row in new_state))
    return neighbors

def reconstruct_path(came_from, current):
    """Reconstruct path from start to goal state."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def a_star(start):
    """A* search to solve the 8 puzzle using Manhattan distance heuristic."""
    open_set = []
    heapq.heappush(open_set, (manhattan_distance(start), 0, start))
   
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start)}
   
    while open_set:
        _, current_g, current = heapq.heappop(open_set)
       
        if current == GOAL_STATE:
            return reconstruct_path(came_from, current)
       
        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor)
                heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))
   
    return None  # No solution found

def print_path(path):
    """Print the sequence of states leading to the solution."""
    for step, state in enumerate(path):
        print(f"Step {step}:")
        for row in state:
            print(row)
        print()

# Example usage
if __name__ == "__main__":
    start_state = ((2, 8, 3),
                   (1, 6, 4),
                   (7, 0, 5))
   
    solution_path = a_star(start_state)
   
    if solution_path:
        print(f"Solution found in {len(solution_path)-1} moves:")
        print_path(solution_path)
    else:
        print("No solution found.")
      ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
OUTPUT:
Step 1:
(2, 8, 3)
(1, 0, 4)
(7, 6, 5)

Step 2:
(2, 0, 3)
(1, 8, 4)
(7, 6, 5)

Step 3:
(0, 2, 3)
(1, 8, 4)
(7, 6, 5)

Step 4:
(1, 2, 3)
(0, 8, 4)
(7, 6, 5)

Step 5:
(1, 2, 3)
(8, 0, 4)
(7, 6, 5)

