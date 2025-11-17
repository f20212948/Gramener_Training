import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score , classification_report

# Step 1: Load dataset
df = pd.read_csv("diabetes.csv")

print("Dataset shape:", df.shape)
print(df.head())

# Step 2: Split features (X) and target (y)
# Assuming "Outcome" column exists, we will predict it
X = df.drop("Outcome", axis=1)   # Features
y = df["Outcome"]                # Target (we treat it as regression)

# Step 3: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 4: Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Make predictions
y_pred = model.predict(X_test)

# Step 6: Evaluate model
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R² Score:", r2_score(y_test, y_pred))

print("\nPredictions\n")
results_df = X_test.copy()
results_df["Actual Values"] = y_test.values
results_df["Predicted Values"] = y_pred
print(results_df)


# Step 7: Plot Actual vs Predicted
plt.scatter(y_test, y_pred, color="blue")
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Linear Regression - Actual vs Predicted")
plt.show()
