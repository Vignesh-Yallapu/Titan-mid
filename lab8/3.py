import numpy as np

class BikeRentalMDP:
    def __init__(self):
        self.max_bikes = 20
        self.demand = [3, 4]
        self.return_bikes = [3, 2]
        self.discount_rate = 0.9
        self.parking_fee = 4
        self.parking_limit = 10

    def get_next_state(self, current_state, action):
        loc1_bikes, loc2_bikes = current_state
        if action > 0:
            if action == 1:
                loc1_bikes -= 1
                loc2_bikes += 1
                action -= 1
            else:
                loc1_bikes -= action
                loc2_bikes += action
        elif action < 0:
            loc1_bikes -= action
            loc2_bikes += -action

        updated_loc1 = min(max(loc1_bikes + self.return_bikes[0] - self.demand[0], 0), self.max_bikes)
        updated_loc2 = min(max(loc2_bikes + self.return_bikes[1] - self.demand[1], 0), self.max_bikes)

        return (updated_loc1, updated_loc2)

    def calculate_parking_fee(self, current_state):
        cost = 0
        if current_state[0] > self.parking_limit:
            cost += self.parking_fee
        if current_state[1] > self.parking_limit:
            cost += self.parking_fee
        return cost

    def calculate_reward(self, current_state, action):
        rented_bikes = min(current_state[0] + self.return_bikes[0], self.demand[0]) + \
                       min(current_state[1] + self.return_bikes[1], self.demand[1])
        
        transfer_cost = max(0, (abs(action) - 1) * 2)
        
        return rented_bikes * 10 - transfer_cost - self.calculate_parking_fee(current_state)

    def policy_iteration(self):
        all_states = [(x1, x2) for x1 in range(self.max_bikes + 1) for x2 in range(self.max_bikes + 1)]
        policy = {state: 0 for state in all_states}
        value_func = {state: 0 for state in all_states}
        tolerance = 1e-6

        while True:
            while True:
                max_diff = 0
                for state in all_states:
                    old_value = value_func[state]
                    action = policy[state]
                    next_state = self.get_next_state(state, action)
                    value_func[state] = self.calculate_reward(state, action) + \
                        self.discount_rate * value_func[next_state]
                    max_diff = max(max_diff, abs(old_value - value_func[state]))
                if max_diff < tolerance:
                    break

            stable_policy = True
            for state in all_states:
                old_action = policy[state]

                action_vals = []
                for action in range(-5, 6):
                    next_state = self.get_next_state(state, action)
                    action_value = self.calculate_reward(state, action) + \
                        self.discount_rate * value_func[next_state]
                    action_vals.append(action_value)

                optimal_action = np.argmax(action_vals) - 5
                policy[state] = optimal_action

                if old_action != policy[state]:
                    stable_policy = False

            if stable_policy:
                break

        return policy, value_func

bike_rental_mdp = BikeRentalMDP()
final_policy, final_value_func = bike_rental_mdp.policy_iteration()

print("Optimal Policy:", final_policy)
print("Optimal Value Function:", final_value_func)
