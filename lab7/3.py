import os
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(0)

class NonStationaryEnvironment:
    """Simulated non-stationary environment where the success probabilities evolve over time."""

    def _init_(self, n_actions, stddev=0.01):
        self.n_actions = n_actions  # Number of actions
        # Initialize mean rewards to be equal (e.g., 0.5)
        self.probs = np.ones(n_actions) * 0.5
        self.stddev = stddev  # Standard deviation for the random walk

    def step(self, action):
        # Pull arm and get stochastic reward (1 for success, 0 for failure)
        reward = 1 if np.random.random() < self.probs[action] else 0
        # Update the probabilities (random walk) for each arm
        self.probs += np.random.normal(0, self.stddev, self.n_actions)
        # Ensure probabilities remain between 0 and 1
        self.probs = np.clip(self.probs, 0, 1)
        return reward

class Agent:

    def _init_(self, nActions, eps):
        self.nActions = nActions  # Number of actions
        self.eps = eps  # Probability of exploration
        self.n = np.zeros(nActions, dtype=int)  # Action counts (fix applied here)
        self.Q = np.zeros(nActions, dtype=float)  # Action-value estimates

    def update_Q(self, action, reward):
        # Increment action count
        self.n[action] += 1
        # Update Q-value for action using incremental update rule
        self.Q[action] += (1.0 / self.n[action]) * (reward - self.Q[action])

    def get_action(self):
        # Epsilon-greedy action selection
        if np.random.random() < self.eps:  # Explore
            return np.random.randint(self.nActions)
        else:  # Exploit
            return np.random.choice(np.flatnonzero(self.Q == self.Q.max()))


def experiment(n_actions, N_episodes, eps, stddev):
    """Run a multi-armed bandit simulation in a non-stationary environment."""
    env = NonStationaryEnvironment(n_actions, stddev)  # Initialize environment
    agent = Agent(n_actions, eps)  # Initialize agent
    actions, rewards = [], []
    for episode in range(N_episodes):
        action = agent.get_action()  # Choose action
        reward = env.step(action)  # Take step and receive reward
        agent.update_Q(action, reward)  # Update Q-value estimate
        actions.append(action)
        rewards.append(reward)
    return np.array(actions), np.array(rewards)


# Settings
n_actions = 10  # Number of bandit arms
N_steps = 500  # Number of steps per experiment
N_experiments = 10_00  # Number of experiments
eps = 0.1  # Exploration probability
stddev = 0.01  # Standard deviation for the random walk
save_fig = True
output_dir = os.path.join(os.getcwd(), "output")

# Run non-stationary bandit experiments
print("Running non-stationary bandits with nActions = {}, eps = {}, stddev = {}".format(n_actions, eps, stddev))
R = np.zeros((N_steps,))  # Reward history
A = np.zeros((N_steps, n_actions))  # Action history

for i in range(N_experiments):
    actions, rewards = experiment(n_actions, N_steps, eps, stddev)
    if (i + 1) % (N_experiments / 100) == 0:
        print("[Experiment {}/{}] ".format(i + 1, N_experiments) +
              "n_steps = {}, reward_avg = {}".format(N_steps, np.sum(rewards) / len(rewards)))
    R += rewards  # Sum rewards over all experiments
    for j, a in enumerate(actions):
        A[j][a] += 1  # Track action counts

# Plot average rewards
# Plot average rewards
R_avg = R / float(N_experiments)
plt.plot(R_avg, ".")
plt.xlabel("Step")
plt.ylabel("Average Reward")
plt.grid()
plt.xlim([1, N_steps])

if save_fig:
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    plt.savefig(os.path.join(output_dir, "nonstat_rewards.png"), bbox_inches="tight")
plt.show()  # Show plot to debug
plt.close()

# Plot action selection percentages
for i in range(n_actions):
    A_pct = 100 * A[:, i] / N_experiments
    steps = list(np.array(range(len(A_pct))) + 1)
    plt.plot(steps, A_pct, "-", linewidth=4, label="Arm {}".format(i + 1))
plt.xlabel("Step")
plt.ylabel("Count Percentage (%)")
plt.legend(loc='upper left', shadow=True)
plt.xlim([1, N_steps])
plt.ylim([0, 100])

if save_fig:
    plt.savefig(os.path.join(output_dir, "nonstat_actions.png"), bbox_inches="tight")
plt.show()  # Show plot to debug
plt.close()