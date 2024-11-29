import numpy as np
from math import factorial, exp

MAX_BIKES = 20
MAX_MOVE = 5
RENT_REWARD = 10
MOVE_COST = 2
DISCOUNT = 0.9
POISSON_UPPER_LIMIT = 11

def poisson_prob(n, lam):
    return exp(-lam) * (lam**n) / factorial(n)

def poisson_distribution(lam):
    return [poisson_prob(n, lam) for n in range(POISSON_UPPER_LIMIT)]

demand_1 = poisson_distribution(3)
return_1 = poisson_distribution(3)
demand_2 = poisson_distribution(4)
return_2 = poisson_distribution(2)

def next_state(state, demand_1, return_1, demand_2, return_2):
    loc1_bikes = min(MAX_BIKES, state[0] - max(0, demand_1) + return_1)
    loc2_bikes = min(MAX_BIKES, state[1] - max(0, demand_2) + return_2)
    reward = RENT_REWARD * (min(state[0], demand_1) + min(state[1], demand_2))
    return (loc1_bikes, loc2_bikes), reward

def policy_iteration():
    values = np.zeros((MAX_BIKES + 1, MAX_BIKES + 1))
    policy = np.zeros((MAX_BIKES + 1, MAX_BIKES + 1), dtype=int)
    
    poisson_probs = {
        "demand_1": demand_1,
        "return_1": return_1,
        "demand_2": demand_2,
        "return_2": return_2
    }
    
    while True:
        while True:
            delta = 0
            new_values = values.copy()
            for loc1 in range(MAX_BIKES + 1):
                for loc2 in range(MAX_BIKES + 1):
                    state = (loc1, loc2)
                    action = policy[loc1, loc2]
                    value = -MOVE_COST * abs(action)
                    
                    for d1, p_d1 in enumerate(poisson_probs["demand_1"]):
                        for r1, p_r1 in enumerate(poisson_probs["return_1"]):
                            for d2, p_d2 in enumerate(poisson_probs["demand_2"]):
                                for r2, p_r2 in enumerate(poisson_probs["return_2"]):
                                    prob = p_d1 * p_r1 * p_d2 * p_r2
                                    new_state, reward = next_state(
                                        (loc1 - action, loc2 + action), d1, r1, d2, r2
                                    )
                                    value += prob * (reward + DISCOUNT * values[new_state])
                    
                    new_values[loc1, loc2] = value
                    delta = max(delta, abs(values[loc1, loc2] - value))
            values = new_values
            if delta < 1e-4:
                break
        
        stable = True
        for loc1 in range(MAX_BIKES + 1):
            for loc2 in range(MAX_BIKES + 1):
                state = (loc1, loc2)
                old_action = policy[loc1, loc2]
                best_action = None
                best_value = float("-inf")
                
                for action in range(-MAX_MOVE, MAX_MOVE + 1):
                    if 0 <= loc1 - action <= MAX_BIKES and 0 <= loc2 + action <= MAX_BIKES:
                        value = -MOVE_COST * abs(action)
                        for d1, p_d1 in enumerate(poisson_probs["demand_1"]):
                            for r1, p_r1 in enumerate(poisson_probs["return_1"]):
                                for d2, p_d2 in enumerate(poisson_probs["demand_2"]):
                                    for r2, p_r2 in enumerate(poisson_probs["return_2"]):
                                        prob = p_d1 * p_r1 * p_d2 * p_r2
                                        new_state, reward = next_state(
                                            (loc1 - action, loc2 + action), d1, r1, d2, r2
                                        )
                                        value += prob * (reward + DISCOUNT * values[new_state])
                        
                        if value > best_value:
                            best_value = value
                            best_action = action
                
                policy[loc1, loc2] = best_action
                if old_action != best_action:
                    stable = False
        
        if stable:
            break
    
    return values, policy

values, policy = policy_iteration()

print("Optimal Policy:")
print(policy)
print("Value Function:")
print(values)
