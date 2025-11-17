import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mode


num_matches = 20  # Number of matches per series
prob_win = 0.65  # Probability of India winning a match
num_series = 1000  # Number of simulated series

# Binomial distribution parameters: n = 20, p = 0.65 (probability of winning)
wins_in_series = np.random.binomial(n=num_matches, p=prob_win, size=num_series)

plt.figure(figsize=(10, 6))
plt.hist(wins_in_series, bins=np.arange(0, num_matches+2)-0.5, edgecolor='black', alpha=0.7 , color='green')
plt.title("Histogram of Wins in 1000 Simulated T20 Series")
plt.xlabel("Number of Matches Won")
plt.ylabel("Frequency")
plt.xticks(np.arange(0, num_matches+1, 1))
plt.grid(axis='y')
plt.show()


wins_at_least_15 = np.sum(wins_in_series >= 15) / num_series
print(f"Probability of winning at least 15 matches: {wins_at_least_15:.4f}")

mean_wins = np.mean(wins_in_series)
mode_wins = mode(wins_in_series)[0]  # Most likely number of wins (mode)
prob_more_than_15 = np.sum(wins_in_series > 15) / num_series

print(f"Mean number of wins: {mean_wins:.2f}")
print(f"Most likely number of wins (mode): {mode_wins}")
print(f"Probability of winning more than 15 matches: {prob_more_than_15:.4f}")
