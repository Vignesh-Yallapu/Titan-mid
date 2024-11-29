import numpy as np

class GridWorldEnvironment:
    def __init__(self, grid_size, terminal_rewards, step_reward, discount_factor=0.9):
        self.grid_size = grid_size
        self.terminal_rewards = terminal_rewards
        self.step_reward = step_reward
        self.gamma = discount_factor
        self.value_grid = np.zeros(grid_size)
        self.actions = ['up', 'down', 'left', 'right']

    def is_terminal_state(self, position):
        return position in self.terminal_rewards

    def reward(self, position):
        return self.terminal_rewards.get(position, self.step_reward)

    def get_next_position(self, position, action):
        row, col = position
        if action == 'up':
            return max(row - 1, 0), col
        elif action == 'down':
            return min(row + 1, self.grid_size[0] - 1), col
        elif action == 'left':
            return row, max(col - 1, 0)
        elif action == 'right':
            return row, min(col + 1, self.grid_size[1] - 1)

    def value_iteration(self, tolerance=1e-6):
        while True:
            delta = 0
            new_value_grid = np.copy(self.value_grid)

            for row in range(self.grid_size[0]):
                for col in range(self.grid_size[1]):
                    position = (row, col)

                    if self.is_terminal_state(position):
                        continue

                    action_values = []
                    for action in self.actions:
                        next_position = self.get_next_position(position, action)
                        intended_value = 0.8 * self.value_grid[next_position]
                        unintended_left = self.get_next_position(position, 'left')
                        unintended_right = self.get_next_position(position, 'right')
                        unintended_value = 0.1 * (self.value_grid[unintended_left] + self.value_grid[unintended_right])
                        total_value = intended_value + unintended_value
                        action_values.append(total_value)

                    best_action_value = max(action_values)
                    new_value_grid[position] = self.reward(position) + self.gamma * best_action_value
                    delta = max(delta, abs(new_value_grid[position] - self.value_grid[position]))

            self.value_grid = new_value_grid
            if delta < tolerance:
                break

        return self.value_grid


grid_size = (4, 3)
terminal_rewards = {(0, 2): 1, (1, 2): -1}
reward_settings = [-2, 0.1, 0.02, 1]

for reward in reward_settings:
    environment = GridWorldEnvironment(grid_size, terminal_rewards, reward)
    value_function = environment.value_iteration()
    print(f"Optimal Value Function for reward = {reward}:\n{value_function}\n")
