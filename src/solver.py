from src.maze import Maze
from queue import PriorityQueue  # for managing nodes
from decimal import Decimal  # for precise cost calculations

def reconstruct_path_and_calculate_cost(came_from, start, goal):
    current = goal  # Start from the goal and work back to the start
    path = []  # Initialize the path list
    total_cost = Decimal('0.0')  # Initialize total cost with a decimal value of 0
    while current != start:  # Loop until the start cell is reached
        path.append((current, True))  # Add the current cell to the path. True means that it belongs to the optimal path
        previous_node = came_from[current]  # Get the previous cell from the current cell
        
        # Determine movement cost based on the direction (vertical or horizontal)
        if current[0] == previous_node[0]:
            total_cost += Decimal('0.9')  # Horizontal movement cost
        else:
            total_cost += Decimal('1.1')  # Vertical movement cost
        
        current = previous_node  # Move to the next cell in the path towards the starts
    path.append((start, True))  # Finally, add the start cell to the path
    path.reverse()  # Reverse the path to start from the beginning
    return path, total_cost  # Return the constructed path and the total cost
  
def uniform_cost_search(maze):
    came_from = {}  # Map each cell to its predecessor in the path
    path = []  # List to keep track of the path taken
    start = maze.entry_coor  # Starting cell coordinates
    goal = maze.exit_coor  # Goal cell coordinates
    
    # Initialize g_score (cost from start to a cell) for all cells to infinity
    g_score = {(x, y): float('inf') for x in range(maze.num_rows) for y in range(maze.num_cols)}
    g_score[start] = 0  # Cost from start to itself is zero

    pq = PriorityQueue()  # Initialize the priority queue. It consists of (cost, (x, y))
    pq.put((0, start))  # Add the start cell with a priority of 0

    while not pq.empty():
        current = pq.get()[1]  # Get the cell with the lowest cost from the queue
        path.append((current, False))  # Mark the current cell as visited (for path visualization)
        maze.grid[current[0]][current[1]].visited = True  # Mark the cell as visited in the maze grid

        # Check if the current cell is the goal
        if current == goal:
            break
        
        # Iterate through all neighbours of the current cell
        for neighbour in maze.find_neighbours(current[0], current[1]):
            # Skip if the neighbour has been visited or if there is a wall between current and neighbour
            if maze.grid[neighbour[0]][neighbour[1]].visited or maze.grid[current[0]][current[1]].is_walls_between(maze.grid[neighbour[0]][neighbour[1]]):
                continue
            
            cost = 1.1 if neighbour[0] == current[0] else 0.9  # Determine the movement cost to the neighbour
            tentative_g_score = g_score[current] + cost  # Calculate tentative cost from start to the neighbour

            # If this path to neighbour is better than any previous one, record it
            if tentative_g_score < g_score[neighbour]:
                g_score[neighbour] = tentative_g_score
                came_from[neighbour] = current  # Record the path
                pq.put((g_score[neighbour], neighbour))  # Add the neighbour to the queue with its updated cost
    
    # After exploring all paths, reconstruct the optimal path and calculate its cost
    found_path, found_cost = reconstruct_path_and_calculate_cost(came_from, start, goal)
    path.extend(found_path)  # Combine the explored path with the optimal path for visualization                                    
    return [path, found_path, found_cost]

# Calculate the heuristic as the Manhattan distance with different costs for horizontal and vertical moves
def heuristic(cell_1, cell_2):
    x_1, y_1 = cell_1
    x_2, y_2 = cell_2
    return (abs(x_1 - x_2) * 0.9 ) + (abs(y_1 - y_2) * 1.1)

def a_star_search(maze, h):
    came_from = {}   # Map each cell to its predecessor in the path
    path = []   # List to keep track of the path taken
    start = maze.entry_coor  # Starting cell coordinates
    goal = maze.exit_coor  # Goal cell coordinates
    
    # Initialize g_score (cost from start to a cell) and f_score (estimated total cost from start to goal through a cell) for all cells to infinity
    g_score = {(x, y): float('inf') for x in range(maze.num_rows) for y in range(maze.num_cols)}
    g_score[start] = 0  # Cost from start to itself is zero
    f_score = {(x, y): float('inf') for x in range(maze.num_rows) for y in range(maze.num_cols)}
    start_heuristic = h(start, goal)  # Calculate the heuristic cost from start to goal
    f_score[start] = start_heuristic  # Initialize the f_score of the start cell (0 + heuristic)

    pq = PriorityQueue()  # Initialize the priority queue (f_score, heuristicm, (x, y))
    pq.put((f_score[start], start_heuristic, start))  # Add the start cell with its f_score to the queue

    while not pq.empty():
        current = pq.get()[2]  # Get the cell with the lowest f_score from the queue
        path.append((current, False))  # Mark the current cell as visited (for path visualization)
        maze.grid[current[0]][current[1]].visited = True  # Mark the cell as visited in the maze grid

        # Check if the current cell is the goal
        if current == goal:
            break
        
        # Iterate through all neighbours of the current cell
        for neighbour in maze.find_neighbours(current[0], current[1]):
            # Skip if the neighbour has been visited or if there is a wall between current and neighbour
            if maze.grid[neighbour[0]][neighbour[1]].visited or maze.grid[current[0]][current[1]].is_walls_between(maze.grid[neighbour[0]][neighbour[1]]):
                continue
            
            cost = 1.1 if neighbour[0] == current[0] else 0.9  # Determine the movement cost to the neighbour
            tentative_g_score = g_score[current] + cost  # Calculate tentative cost from start to the neighbour
            tentative_f_score = tentative_g_score + h(neighbour, goal)  # Add heuristic to get f_score for the neighbour

            # If this path to neighbour is better than any previous one, record it
            if tentative_f_score < f_score[neighbour]:
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_f_score
                came_from[neighbour] = current
                if not any(neighbour == item[1] for item in pq.queue):
                    pq.put((f_score[neighbour], h(neighbour, goal), neighbour))  # Add it to the priority queue with its f_score

    # After exploring all paths, reconstruct the optimal path and calculate its cost
    optimal_path, optimal_cost = reconstruct_path_and_calculate_cost(came_from, start, goal)                
    path.extend(optimal_path)  # Combine the explored path with the optimal path for visualization
    return [path, optimal_path, optimal_cost]
