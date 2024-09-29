import numpy as np
from hmmlearn.hmm import GaussianHMM
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
#...............................................................................

 # Part 1: Data Collection and Preprocessing

  # (a) Data Acquisition:

    # Download and preprocess financial data
    ticker = 'GOOGL'
    start_date = '2010-01-01'
    end_date = '2023-01-01'
    # Download historical stock data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date)

  # (b) Preprocessing:

    # Calculate daily returns from adjusted closing prices
    data['Returns'] = data['Adj Close'].pct_change().dropna()
    # Drop rows with missing data
    data = data.dropna()

#...............................................................................

# Part 2: Gaussian Hidden Markov Model

 # (a) Fitting the Model:

    # Fit Gaussian HMM to the returns data
    num_hidden_states = 2
    # Reshape returns data for HMM fitting
    returns = data['Returns'].values.reshape(-1, 1)
    # Define and fit the Gaussian HMM model
    model = GaussianHMM(n_components=num_hidden_states, covariance_type="full", n_iter=1000)
    model.fit(returns)
    # Predict the hidden states
    hidden_states = model.predict(returns)

#...............................................................................

# Part 3: Interpretation and Inference

 # (a) Inferred Hidden States:

    # Analyze and visualize the hidden states
    # Add hidden states to the dataframe
    data['Hidden State'] = hidden_states

    # Plot the Adjusted Close price with color-coded hidden states
    plt.figure(figsize=(14, 7))
    for i in range(model.n_components):
        state = data[data['Hidden State'] == i]
        plt.plot(state.index, state['Adj Close'], label=f'State {i}', linestyle='-', marker='o')

    plt.title(f"{ticker} Stock Price and Hidden States")
    plt.xlabel('Date')
    plt.ylabel('Adjusted Close Price')
    plt.legend()
    plt.show()

#...............................................................................

# Part 4: Evaluation and Visualization

 # (a) Visualization:

    # Visualize returns with hidden states
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Returns'], label='Daily Returns')
    colors = ['red' if state == 0 else 'green' for state in hidden_states]
    plt.scatter(data.index, data['Returns'], c=colors, label='Hidden States', alpha=0.5)
    plt.title(f"{ticker} Returns and Hidden States")
    plt.xlabel('Date')
    plt.ylabel('Returns')
    plt.show()
#...............................................................................


 # (b) of part 2 & 3 Parameter Analysis & Transition Matrix respectively:

    # Analyze the model parameters and transition matrix
    # Print mean and variance of each hidden state
    for i in range(model.n_components):
        print(f"Hidden State {i}")
        print(f"Mean = {model.means_[i]}")
        print(f"Variance = {np.diag(model.covars_[i])}")
        print()

    # Display the transition matrix
    print("Transition Matrix:")
    print(model.transmat_)
#...............................................................................

# Part 5: Conclusions and Insights

 # Market Regime Interpretation and Future Prediction:

    # Predict the most likely future state
    current_state = hidden_states[-1]
    future_state_prob = model.transmat_[current_state]
    predicted_state = np.argmax(future_state_prob)
    print(f"The most likely future hidden state is: {predicted_state}")