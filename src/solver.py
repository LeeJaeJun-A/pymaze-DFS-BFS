from src.maze import Maze
from queue import PriorityQueue # sjaqjnjs
from decimal import Decimal # sjaqjnjs
    
def uniform_cost_search(maze):
    came_from = {}
    path = []
    start = maze.entry_coor
    goal = maze.exit_coor
    
    g_score = {(x, y): float('inf') for x in range(maze.num_rows) for y in range(maze.num_cols)}
    g_score[start] = 0

    pq = PriorityQueue()
    pq.put((g_score[start], start))

    while not pq.empty():
        current = pq.get()[1]
        path.append((current, False))
        maze.grid[current[0]][current[1]].visited = True

        if current == goal:
            break
        
        for neighbour in maze.find_neighbours(current[0], current[1]):
            if maze.grid[neighbour[0]][neighbour[1]].visited:
                continue
            if maze.grid[current[0]][current[1]].is_walls_between(maze.grid[neighbour[0]][neighbour[1]]):
                continue
            
            cost = 1.1 if neighbour[0] == current[0] else 0.9
            temp_g_score = g_score[current] + cost

            if temp_g_score < g_score[neighbour]:
                g_score[neighbour] = temp_g_score
                came_from[neighbour] = current
                if not any(neighbour == item[1] for item in pq.queue):
                    pq.put((g_score[neighbour], neighbour))
            
    found_path = []
    found_cost = 0
    cell = goal
    while cell != start:
        found_path.append((cell, True))
        previous_cell = came_from[cell]

        if cell[0] == previous_cell[0]:
            found_cost += Decimal('0.9')
        else:
            found_cost += Decimal('1.1')
        cell = previous_cell
    found_path.append((start, True))
    found_path.reverse()
    path.extend(found_path)                  
    return [path, found_path, found_cost]

def heuristic(cell_1, cell_2):
    x_1, y_1 = cell_1
    x_2, y_2 = cell_2
    return (abs(x_1 - x_2) * 0.9 ) + (abs(y_1 - y_2) * 1.1)

def a_star_search(maze, h):
    came_from = {}
    path = []
    start = maze.entry_coor
    goal = maze.exit_coor
    
    g_score = {(x, y): float('inf') for x in range(maze.num_rows) for y in range(maze.num_cols)}
    g_score[start] = 0

    f_score = {(x, y): float('inf') for x in range(maze.num_rows) for y in range(maze.num_cols)}
    start_heuristic = h(start, goal)
    f_score[start] = start_heuristic


    pq = PriorityQueue()
    pq.put((start_heuristic, start_heuristic, start))

    while not pq.empty():
        current = pq.get()[2]
        path.append((current, False))
        maze.grid[current[0]][current[1]].visited = True

        if current == goal:
            break
        
        for neighbour in maze.find_neighbours(current[0], current[1]):
            if maze.grid[neighbour[0]][neighbour[1]].visited:
                continue
            if maze.grid[current[0]][current[1]].is_walls_between(maze.grid[neighbour[0]][neighbour[1]]):
                continue
            
            cost = 1.1 if neighbour[0] == current[0] else 0.9
            temp_g_score = g_score[current] + cost
            temp_f_score = temp_g_score + h(neighbour, goal)

            if temp_f_score < f_score[neighbour]:
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_f_score
                came_from[neighbour] = current
                if not any(neighbour == item[1] for item in pq.queue):
                    pq.put((f_score[neighbour], h(neighbour, goal), neighbour))
    optimal_path = []
    optimal_cost = 0
    cell = goal
    while cell != start:
        optimal_path.append((cell, True))
        previous_cell = came_from[cell]

        if cell[0] == previous_cell[0]:
            optimal_cost += Decimal('0.9')
        else:
            optimal_cost += Decimal('1.1')
        cell = previous_cell
    optimal_path.append((start, True))
    optimal_path.reverse()                  
    path.extend(optimal_path)
    return [path, optimal_path, optimal_cost]
