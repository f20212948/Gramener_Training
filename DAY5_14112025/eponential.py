import numpy as np
import matplotlib.pyplot as plt

# Generate data from an Exponential Distribution
# scale = 1/lambda (mean waiting time), size = number of samples
data = np.random.exponential(scale=5, size=1000)

# Plotting the exponential distribution
plt.figure(figsize=(8, 5))
plt.hist(data, bins=30, density=True)
plt.title("Exponential Distribution Example")
plt.xlabel("Time (e.g., waiting time, response time)")
plt.ylabel("Density")
plt.grid(True)

plt.show()