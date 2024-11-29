import numpy as np

rows, cols = 4, 3
terminal_states = {(0, 2): 1, (1, 2): -1}
ACTIONS = ["up", "down", "left", "right"]
DISCOUNT = 0.9

ACTION_PROBS = {
    "up": (0.8, "left", "right"),
    "down": (0.8, "right", "left"),
    "left": (0.8, "down", "up"),
    "right": (0.8, "up", "down"),
}

def get_reward(state, r_s):
    return terminal_states.get(state, r_s)

def next_state(state, action):
    row, col = state
    if action == "up" and row > 0:
        row -= 1
    elif action == "down" and row < rows - 1:
        row += 1
    elif action == "left" and col > 0:
        col -= 1
    elif action == "right" and col < cols - 1:
        col += 1
    return (row, col)

def value_iteration(r_s, threshold=1e-6):
    values = np.zeros((rows, cols))
    policy = np.empty((rows, cols), dtype=object)

    while True:
        delta = 0
        new_values = values.copy()

        for row in range(rows):
            for col in range(cols):
                state = (row, col)

                if state in terminal_states:
                    new_values[state] = get_reward(state, r_s)
                    continue

                action_values = []
                for action in ACTIONS:
                    intended_next = next_state(state, action)
                    intended_value = 0.8 * values[intended_next]

                    unintended_next1 = next_state(state, ACTION_PROBS[action][1])
                    unintended_next2 = next_state(state, ACTION_PROBS[action][2])
                    unintended_value = 0.1 * (values[unintended_next1] + values[unintended_next2])

                    action_value = get_reward(state, r_s) + DISCOUNT * (intended_value + unintended_value)
                    action_values.append(action_value)

                best_action_value = max(action_values)
                best_action = ACTIONS[action_values.index(best_action_value)]
                new_values[state] = best_action_value
                policy[state] = best_action

                delta = max(delta, abs(new_values[state] - values[state]))

        values = new_values
        if delta < threshold:
            break

    return values, policy

rewards = [-2, 0.1, 0.02, 1.0]
for r_s in rewards:
    print(f"Running value iteration for r(s) = {r_s}...")
    values, policy = value_iteration(r_s)
    print(f"Optimal Value Function for r(s) = {r_s}:\n{values}")
    print(f"Optimal Policy for r(s) = {r_s}:\n{policy}\n")
