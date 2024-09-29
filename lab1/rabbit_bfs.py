from collections import deque

def bfs(start, goal):

    queue = deque([(start, [])])
    visited = set()
    visited.add(start)

    while queue:
        (state, path) = queue.popleft()

        path = path + [state]
        if state == goal:
            print(len(visited))
            return path
        
        for next_state in get_next_states(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path))
    
    return None

def get_next_states(state):
    next_states = []
    stones = list(state)
    blank = stones.index('_')


    for i in range(len(stones)):
        if stones[i] == 'E':
            
            if blank > i and (blank - i == 1 or blank - i == 2):

                nextston = stones[:]
                nextston[blank], nextston[i] = nextston[i], nextston[blank]
                next_states.append(tuple(nextston))
            elif blank > i + 1 and stones[i + 1] == 'W' and (blank - i == 2):

                nextston = stones[:]
                nextston[blank], nextston[i] = nextston[i], nextston[blank]
                next_states.append(tuple(nextston))
        elif stones[i] == 'W':

            if blank < i and (i - blank == 1 or i - blank == 2):
 
                nextston = stones[:]
                nextston[blank], nextston[i] = nextston[i], nextston[blank]
                next_states.append(tuple(nextston))
            elif blank < i - 1 and stones[i - 1] == 'E' and (i - blank == 2):

                nextston = stones[:]
                nextston[blank], nextston[i] = nextston[i], nextston[blank]
                next_states.append(tuple(nextston))

    return next_states




start = ('E', 'E', 'E', '_', 'W', 'W', 'W')
goal = ('W', 'W', 'W', '_', 'E', 'E', 'E')

solution = bfs(start, goal)

if solution:
    print("the rabbits cross each other without stepping into the water")
    for step in solution:
        print(step)
    
else:
    print("the rabbits can not cross each other without stepping into the water")