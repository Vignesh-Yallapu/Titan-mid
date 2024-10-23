function [reward] = bandit_nonstat(action)
    % bandit_nonstat Simulates a non-stationary 10-armed bandit environment
    % Inputs:
    %   action - selected arm (integer between 1 and 10)
    % Outputs:
    %   reward - stochastic reward (1 for success, 0 for failure)
    
    persistent mean_rewards;  % Persistent variable to store mean rewards for each arm
    persistent stddev;        % Standard deviation for random walk
    persistent n_arms;        % Number of arms

    if isempty(mean_rewards)
        % Initialize parameters on the first run
        n_arms = 10;  % 10-armed bandit
        stddev = 0.01;  % Standard deviation for random walk
        mean_rewards = 0.5 * ones(1, n_arms);  % Initialize mean rewards to 0.5 for each arm
    end

    % Perform a random walk for each arm (random increment with mean 0 and stddev 0.01)
    mean_rewards = mean_rewards + normrnd(0, stddev, [1, n_arms]);

    % Ensure mean rewards are within the [0, 1] range
    mean_rewards = max(0, min(mean_rewards, 1));

    % Return a stochastic reward based on the selected action's mean reward
    reward = rand() < mean_rewards(action);  % Return 1 for success, 0 for failure
end