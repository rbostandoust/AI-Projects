import math
# depth-limited dfs
def dls_solver(maze, limit):
    return []

def iterative_dfs_solver(maze):
    return []

def dfs_solver(maze):
    return []

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
        if(u == maze.goal):
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
