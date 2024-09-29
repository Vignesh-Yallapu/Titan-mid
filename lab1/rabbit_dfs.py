from collections import deque

def bfs(start, goal):

    stack = deque([(start, [])])
    visited = set()
    visited.add(start)

    while stack:
        (state, path) = stack.pop()
        
        path = path + [state]
        if state == goal:
            print(len(visited))
            return path
        
        for next_state in get_next_states(state):
            if next_state not in visited:
                visited.add(next_state)
                stack.append((next_state, path))
    
    return None

def get_next_states(state):
    next_states = []
    stones = list(state)
    empty_index = stones.index('_')


    for i in range(len(stones)):
        if stones[i] == 'E':

            if empty_index > i and (empty_index - i == 1 or empty_index - i == 2):

                new_stones = stones[:]
                new_stones[empty_index], new_stones[i] = new_stones[i], new_stones[empty_index]
                next_states.append(tuple(new_stones))
            elif empty_index > i + 1 and stones[i + 1] == 'W' and (empty_index - i == 2):

                new_stones = stones[:]
                new_stones[empty_index], new_stones[i] = new_stones[i], new_stones[empty_index]
                next_states.append(tuple(new_stones))
        elif stones[i] == 'W':

            if empty_index < i and (i - empty_index == 1 or i - empty_index == 2):

                new_stones = stones[:]
                new_stones[empty_index], new_stones[i] = new_stones[i], new_stones[empty_index]
                next_states.append(tuple(new_stones))
            elif empty_index < i - 1 and stones[i - 1] == 'E' and (i - empty_index == 2):

                new_stones = stones[:]
                new_stones[empty_index], new_stones[i] = new_stones[i], new_stones[empty_index]
                next_states.append(tuple(new_stones))

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