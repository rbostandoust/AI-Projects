import math
# depth-limited dfs
def dls_solver(maze, limit):
    visited = []
    parent = {}
    cell_limit = {}
    queue = []
    result = []
    queue.append(maze.start)
    cell_limit[maze.start] = limit
    while(len(queue) != 0):
        u = queue.pop()
        limit = limit - 1
        visited.append(u)
        neighbors = maze.get_neighbors(u)
        if u == maze.goal:
            break
        if cell_limit[u] > 0:    
            for i in neighbors:
                if not maze.check_wall(u, i):
                    if i not in visited:
                        parent[i] = u
                        cell_limit[i] = limit
                        if i in queue:
                            queue = [x for x in queue if x != i]
                        queue.append(i)
    while u != maze.start:
        result.append(u)
        u = parent[u]
    result.append(maze.start)
    result.reverse()
    if maze.goal not in result:
        return []
    return result

def iterative_dfs_solver(maze):
    result = []
    for i in range(1, maze.ncols * maze.nrows):
        result = dls_solver(maze, i)
        if not result == []:
            break
    return result

def dfs_solver(maze):
    visited = []
    parent = {}
    queue = []
    result = []
    queue.append(maze.start)
    while(len(queue) != 0):
        u = queue.pop()
        visited.append(u)
        neighbors = maze.get_neighbors(u)
        if u == maze.goal:
            break
        for i in neighbors:
            if not maze.check_wall(u, i):
                if i not in visited:
                    parent[i] = u
                    if i in queue:
                        queue = [x for x in queue if x != i]
                    queue.append(i)
    while u != maze.start:
        result.append(u)
        u = parent[u]
    result.append(maze.start)
    result.reverse()
    return result

def bfs_solver(maze):
    visited = []
    queue = []
    parent = {}
    result = []
    queue.append(maze.start)
    while len(queue) != 0:
        u = queue.pop(0)
        visited.append(u)
        neighbors = maze.get_neighbors(u)
        if u == maze.goal:
            break
        for i in neighbors:
            if not maze.check_wall(u , i):
                if i not in visited:
                    queue.append(i)
                    parent[i] = u
                    visited.append(i)
    
    while u != maze.start:
        result.append(u)
        u = parent[u]
    result.append(maze.start)
    result.reverse()
    return result

def astar_heuristic(maze, cell):
    return (int)(math.sqrt(pow((cell[0] - maze.goal[0]), 2) + pow((cell[1] - maze.goal[1]), 2)))

def find_min(maze, sample_list, distance):
    min_distance = astar_heuristic(maze, sample_list[0]) + distance[sample_list[0]]
    min_id = 0
    for i in range (1, len(sample_list)):
        new_distance = astar_heuristic(maze, sample_list[i]) + distance[sample_list[i]]
        if(min_distance > new_distance):
            min_distance = new_distance
            min_id = i
    return min_id


def astar_solver(maze):
    visited = []
    queue = []
    parent = {}
    result = []
    distance = {}
    counter = 0
    distance[maze.start] = counter
    queue.append(maze.start)
    while len(queue) != 0:
        counter = counter + 1
        min_id = find_min(maze, queue, distance)
        u = queue.pop(min_id)
        visited.append(u)
        neighbors = maze.get_neighbors(u)
        if(u == maze.goal):
            break
        for i in neighbors:
            if not maze.check_wall(u , i):
                if i not in visited:
                    queue.append(i)
                    parent[i] = u
                    visited.append(i)
                    distance[i] = counter

    while u != maze.start:
        result.append(u)
        u = parent[u]
    result.append(maze.start)
    result.reverse()
    return result
