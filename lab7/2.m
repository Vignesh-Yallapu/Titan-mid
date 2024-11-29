% Initialize parameters
bandit_probs = [0.4, 0.6];  % Success probabilities for binaryBanditA and binaryBanditB
N_steps = 1000;  % Number of episodes
eps = 0.1;  % Epsilon for exploration
nActions = length(bandit_probs);  % Number of actions (binaryBanditA, binaryBanditB)

% Initialize agent parameters
Q = zeros(1, nActions);  % Action-value estimates
n = zeros(1, nActions);  % Number of times each action has been taken
actions = zeros(1, N_steps);  % Store actions
rewards = zeros(1, N_steps);  % Store rewards

% Function to simulate binary bandit
binaryBandit = @(p) rand() < p;  % Returns 1 with probability p, otherwise 0

% Run epsilon-greedy experiment
for step = 1:N_steps
    % Epsilon-greedy action selection
    if rand() < eps
        action = randi(nActions);  % Explore: choose random action
    else
        [~, action] = max(Q);  % Exploit: choose action with highest Q-value
    end

    % Get reward from the selected bandit
    reward = binaryBandit(bandit_probs(action));

    % Update the count for the selected action
    n(action) = n(action) + 1;

    % Update Q-value estimate using incremental mean formula
    Q(action) = Q(action) + (1 / n(action)) * (reward - Q(action));

    % Store action and reward
    actions(step) = action;
    rewards(step) = reward;
end

% Plot the average reward over time
avg_reward = cumsum(rewards) ./ (1:N_steps);
figure;
plot(1:N_steps, avg_reward);
xlabel('Step');
ylabel('Average Reward');
title(['Epsilon-Greedy: Epsilon = ', num2str(eps)]);
grid on;

% Plot histogram of action selection
figure;
histogram(actions, 'BinEdges', 0.5:1:nActions+0.5, 'Normalization', 'count');
xlabel('Action (1 = Bandit A, 2 = Bandit B)');
ylabel('Count');
title('Action Selection Histogram');
grid on;