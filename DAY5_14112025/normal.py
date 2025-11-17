import numpy as np
import matplotlib.pyplot as plt

# Generate sample data for a normal distribution (bell curve)
# loc = mean, scale = standard deviation, size = number of data points
data = np.random.normal(loc=50, scale=10, size=1000)

# Plotting the histogram (bell curve)
plt.figure(figsize=(8, 5))
plt.hist(data, bins=30, density=True)
plt.title("Bell Curve (Normal Distribution) - Sales Example")
plt.xlabel("Sales Units")
plt.ylabel("Density")
plt.grid(True)

plt.show()