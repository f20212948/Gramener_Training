import numpy as np
import matplotlib.pyplot as plt

# Binomial Distribution Parameters
n = 10      # number of trials
p = 0.5     # probability of success
size = 1000 # number of samples

# Generate binomial data
data = np.random.binomial(n=n, p=p, size=size)

# Plotting the distribution
plt.figure(figsize=(8, 5))
plt.hist(data, bins=range(n+2), density=True, align='left')
plt.title("Binomial Distribution Example")
plt.xlabel("Number of Successes")
plt.ylabel("Probability")
plt.grid(True)

plt.show()