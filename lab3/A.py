import time
import heapq
import copy

class MarbleSolitaire:
    initial_state = [
        [-1,-1, 1, 1, 1,-1,-1],
        [-1,-1, 1, 1, 1,-1,-1],
        [ 1, 1, 1, 1, 1, 1, 1],
        [ 1, 1, 1, 0, 1, 1, 1],
        [ 1, 1, 1, 1, 1, 1, 1],
        [-1,-1, 1, 1, 1,-1,-1],
        [-1,-1, 1, 1, 1,-1,-1]
    ]

    goal_state = [
        [-1,-1, 0, 0, 0,-1,-1],
        [-1,-1, 0, 0, 0,-1,-1],
        [ 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 1, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0],
        [-1,-1, 0, 0, 0,-1,-1],
        [-1,-1, 0, 0, 0,-1,-1]
    ]

    def __init__(self):
        pass

    def is_goal_state(self, state) -> bool:
        return state == self.goal_state

    def display_board(self, curr_state) -> None:
        # Display the current state of the board
        for row in curr_state:
            print(' '.join(map(str, row)))
        print()

    def is_valid_position(self, row, col) -> bool:
        return 0 <= row < 7 and 0 <= col < 7

    def is_valid_move(self, curr_state, start_row, start_col, end_row, end_col) -> bool:
        if not (self.is_valid_position(start_row, start_col) and self.is_valid_position(end_row, end_col)):
            return False
        
        if (
            abs(start_row - end_row) == 2 and start_col == end_col and
            curr_state[(start_row + end_row) // 2][start_col] == 1 and
            curr_state[end_row][end_col] == 0
        ) or (
            abs(start_col - end_col) == 2 and start_row == end_row and
            curr_state[start_row][(start_col + end_col) // 2] == 1 and
            curr_state[end_row][end_col] == 0
        ):
            return True
        return False

    def apply_move(self, current_state, start_row, start_col, end_row, end_col):
        
        if not self.is_valid_move(current_state, start_row, start_col, end_row, end_col):
            print("Invalid move. Please try again.")
            return
        
        curr_state = [list(row) for row in current_state]
        
        curr_state[start_row][start_col] = 0
        curr_state[(start_row + end_row) // 2][(start_col + end_col) // 2] = 0
        curr_state[end_row][end_col] = 1
        return curr_state
    
    def get_next_states(self, current_state):
        new_states = []
        for row in range(len(current_state)):
                for col in range(len(current_state[0])):
                    if current_state[row][col] == 1:
                        for move in [(row - 2, col), (row + 2, col), (row, col - 2), (row, col + 2)]:
                            new_row, new_col = move
                            if self.is_valid_move(current_state, row, col, new_row, new_col):
                                new_state = self.apply_move(current_state, row, col, new_row, new_col)
                                new_states.append(new_state)
                                
        return new_states

    def man_heuristic(self, state) -> int:
        
        center_row, center_col = 7 // 2, 7 // 2
        distance = 0
        for row in range(7):
            for col in range(7):
                if state[row][col] == 1:
                    distance += abs(row - center_row) + abs(col - center_col)
        return distance
    
    def marbles_left_heuristic(self, state) -> int:
        
        marbles = 0
        for row in range(7):
            for col in range(7):
                if state[row][col] == 1:
                    marbles += 1
        return marbles
    
class PriorityQueueAgent:
    def __init__(self, problem):
        self.problem = problem
        self.visited_states = set()

    def search(self):
        states_explored = 1
        initial_state = copy.deepcopy(self.problem.initial_state)
        initial_state_tuple = tuple(map(tuple, initial_state))
        priority_queue = [(0, initial_state_tuple)]
        heapq.heapify(priority_queue)

        while priority_queue:

            path_cost, current_state = heapq.heappop(priority_queue)

            if self.problem.is_goal_state([list(state) for state in current_state]):
                return (path_cost, states_explored)

            current_state_tuple = tuple(map(tuple, current_state))
            if current_state_tuple in self.visited_states:
                continue
            
            self.visited_states.add(current_state_tuple)

            new_states = self.problem.get_next_states([list(state) for state in current_state])

            for new_state in new_states:
                new_state_tuple = tuple(map(tuple, new_state))
                new_cost = path_cost + 1
                if new_state_tuple in self.visited_states:
                    continue
                
                heapq.heappush(priority_queue, (new_cost, new_state_tuple))
                states_explored += 1

        return (None, states_explored)
    
class BestFirstSearchAgent:
    def __init__(self, problem):
        self.problem = problem
        self.visited_states = set()

    def search(self):
        states_explored = 1
        initial_state = copy.deepcopy(self.problem.initial_state)
        initial_state_tuple = tuple(map(tuple, initial_state))
        priority_queue = [(self.problem.man_heuristic(initial_state), 0, initial_state_tuple)]
        heapq.heapify(priority_queue)

        while priority_queue:
            
            _, path_cost, current_state = heapq.heappop(priority_queue)

            if self.problem.is_goal_state([list(state) for state in current_state]):
                return (path_cost, states_explored)

            current_state_tuple = tuple(map(tuple, current_state))
            if current_state_tuple in self.visited_states:
                continue
            
            self.visited_states.add(current_state_tuple)

            new_states = self.problem.get_next_states([list(state) for state in current_state])

            for new_state in new_states:
                new_state_tuple = tuple(map(tuple, new_state))
                new_cost = path_cost + 1
                if new_state_tuple in self.visited_states:
                    continue
                
                found = False
                for i, (heu, cost, state) in enumerate(priority_queue):
                    if state == new_state_tuple:
                        found = True
                        if new_cost < cost:
                            
                            priority_queue[i] = (heu, new_cost, new_state_tuple)
                            heapq.heapify(priority_queue)
                        break
                
                if not found:
                    heapq.heappush(priority_queue, (self.problem.man_heuristic(new_state), new_cost, new_state_tuple))
                    states_explored += 1

        return (None, states_explored)
    
class AStarSearchAgent:
    def __init__(self, problem):
        self.problem = problem
        self.visited_states = set()

    def search(self):
        states_explored = 1
        initial_state = copy.deepcopy(self.problem.initial_state)
        initial_state_tuple = tuple(map(tuple, initial_state))
        priority_queue = [(self.problem.man_heuristic(initial_state), 0, initial_state_tuple)]
        heapq.heapify(priority_queue)

        while priority_queue:
            
            _, path_cost, current_state = heapq.heappop(priority_queue)

            if self.problem.is_goal_state([list(state) for state in current_state]):
                return (path_cost, states_explored)

            current_state_tuple = tuple(map(tuple, current_state))
            if current_state_tuple in self.visited_states:
                continue
            
            self.visited_states.add(current_state_tuple)

            new_states = self.problem.get_next_states([list(state) for state in current_state])

            for new_state in new_states:
                new_state_tuple = tuple(map(tuple, new_state))
                new_cost = path_cost + 1
                if new_state_tuple in self.visited_states:
                    continue
                
                found = False
                for i, (__, cost, state) in enumerate(priority_queue):
                    if state == new_state_tuple:
                        found = True
                        if new_cost < cost:
                            heu = self.problem.man_heuristic(new_state)
                            priority_queue[i] = (heu+new_cost, new_cost, new_state_tuple)
                            heapq.heapify(priority_queue)
                        break
                
                if not found:
                    heapq.heappush(priority_queue, (self.problem.man_heuristic(new_state), new_cost, new_state_tuple))
                    states_explored += 1

        return (None, states_explored)

marble_solitaire = MarbleSolitaire()

selected_agent = input("Select an agent from the following:\n1. Priority queue based agent\n2. Best first search based agent\n3. A* search based agent\n")

if selected_agent == 1:
    agent = PriorityQueueAgent(marble_solitaire)
elif selected_agent == 2:
    agent = BestFirstSearchAgent(marble_solitaire)
elif selected_agent == 3:
    agent = AStarSearchAgent(marble_solitaire)

print("Calculating...")
start_time = time.process_time()
solution = agent.search()
end_time = time.process_time()

if solution[0] is not None:
    print("\nSolution found!\nPath cost:", solution[0], "\nNumber of states explored:", solution[1], "\nTime elapsed:", end_time-start_time)
else:
    print("\nNo solution found.\nNumber of states explored:", solution[1], "\nTime elpased:", end_time-start_time)
