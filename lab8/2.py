import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)  # Seed for reproducibility

class BinaryBandit:
    """A binary bandit returning 1 for success and 0 for failure with a fixed probability."""
    def _init_(self, p):
        self.p = p  # Probability of returning 1 (success)

    def step(self):
        # Returns 1 with probability self.p, otherwise returns 0.
        return 1 if np.random.random() < self.p else 0


class EpsilonGreedyAgent:
    """Epsilon-greedy agent that chooses between two binary bandits."""
    def _init_(self, nActions, eps):
        self.eps = eps  # Probability of exploration
        self.nActions = nActions  # Number of bandit actions (arms)
        self.Q = np.zeros(nActions)  # Estimated value of actions (arms)
        self.n = np.zeros(nActions)  # Number of times each action has been taken

    def update_Q(self, action, reward):
        """Update action-value estimates with the incremental mean formula."""
        self.n[action] += 1  # Increment the count for this action
        self.Q[action] += (1 / self.n[action]) * (reward - self.Q[action])  # Update Q estimate

    def get_action(self):
        """Select an action using epsilon-greedy policy."""
        if np.random.random() < self.eps:
            return np.random.randint(self.nActions)  # Explore: Random action
        else:
            return np.argmax(self.Q)  # Exploit: Select action with highest Q


def experiment(bandit_probs, N_episodes, eps):
    """Run epsilon-greedy experiment on binary bandits."""
    bandits = [BinaryBandit(p) for p in bandit_probs]  # Create bandit instances with success probabilities
    agent = EpsilonGreedyAgent(len(bandit_probs), eps)  # Initialize the agent
    actions, rewards = [], []

    for episode in range(N_episodes):
        action = agent.get_action()  # Choose action (bandit to pull)
        reward = bandits[action].step()  # Get reward from selected bandit
        agent.update_Q(action, reward)  # Update action-value estimate
        actions.append(action)
        rewards.append(reward)

    return np.array(actions), np.array(rewards)


# Parameters
bandit_probs = [0.4, 0.6]  # Success probabilities for binaryBanditA and binaryBanditB
N_steps = 1000  # Number of steps (episodes)
eps = 0.1  # Epsilon for exploration

# Run experiment
actions, rewards = experiment(bandit_probs, N_steps, eps)

# Plot results
plt.plot(np.cumsum(rewards) / (np.arange(N_steps) + 1), label="Average Reward")
plt.xlabel("Step")
plt.ylabel("Average Reward")
plt.title(f"Epsilon-Greedy: Epsilon = {eps}")
plt.grid()
plt.legend()
plt.show()

# Action selection plot
plt.hist(actions, bins=np.arange(-0.5, 2, 1), rwidth=0.5)
plt.xlabel("Action (0 = Bandit A, 1 = Bandit B)")
plt.ylabel("Count")
plt.title("Action Selection Histogram")
plt.grid()
plt.show()