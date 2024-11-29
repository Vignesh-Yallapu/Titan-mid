import numpy as np

class BikeRentalMDP:
    def __init__(self):
        self.max_bikes = 20
        self.demand = [3, 4]
        self.inventory_returns = [3, 2]
        self.discount_rate = 0.9

    def get_next_state(self, current_state, action):
        updated_state = [min(max(current_state[0] + self.inventory_returns[0] - self.demand[0], 0), self.max_bikes),
                         min(max(current_state[1] + self.inventory_returns[1] - self.demand[1], 0), self.max_bikes)]
        updated_state[0] += action
        updated_state[1] -= action
        updated_state[0] = max(0, min(updated_state[0], self.max_bikes))
        updated_state[1] = max(0, min(updated_state[1], self.max_bikes))
        return tuple(updated_state)

    def calculate_reward(self, current_state, action):
        rented_bikes = min(current_state[0] + self.inventory_returns[0], self.demand[0]) + \
                       min(current_state[1] + self.inventory_returns[1], self.demand[1])
        return rented_bikes * 10 - abs(action) * 2

rental_mdp = BikeRentalMDP()
start_state = (10, 10)
move_action = -3
next_state = rental_mdp.get_next_state(start_state, move_action)
reward = rental_mdp.calculate_reward(start_state, move_action)

print(f"Next State: {next_state}, Reward: {reward}")
