

import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.express as px
import os
import joblib
# -----------------------------------
# 1  Data Ingestion (Create + Read)
# -----------------------------------
print("\nData Ingestion\n")

# Create a sample CSV if not exists
csv_file = "./hospital_data.csv"

if not os.path.exists(csv_file):
    print("Creating sample dataset...")
    data_dict = {
"Room_Charges": [2791.82, 4588.95, 4153.83, 2883.46, 6268.16, 6550.16, 2776.1, 3617.81, 2505.45, 2677.05, 3838.71, 5742.0, 7846.19, 7562.2, 3160.4, 2811.75, 3667.68, 6658.68, 2196.75, 6641.0, 4055.83, 2641.43, 7297.98, 6034.78, 6963.29],
"Consultation_Hours": [1.9, 1.8, 3.7, 1.7, 1.8, 4.9, 3.2, 2.4, 4.5, 5.3, 5.7, 5.1, 4.3, 5.6, 3.2, 4.3, 3.9, 2.8, 1.7, 4.2, 1.5, 3.2, 5.3, 2.2, 5.5],
"Num_Tests": [8, 6, 3, 2, 2, 1, 8, 2, 1, 8, 4, 8, 5, 4, 6, 2, 1, 6, 6, 1, 8, 6, 7, 1, 5],
"Days_Admitted": [1, 7, 4, 5, 1, 4, 7, 3, 1, 2, 4, 7, 5, 1, 4, 6, 2, 6, 6, 7, 2, 3, 2, 5, 1],
"Age":[34,23,55,51,48,37,33,31,74,24,23,31,47,49,84,23,45,73,48,77,55,20,40,74,63],
"Total_Bill": [10523.03, 19089.53, 12850.27, 12247.03, 9007.8, 14852.5, 19444.64, 9504.69, 6228.19, 13373.13, 14014.1, 23811.16, 19690.17, 15502.9, 13930.12, 14409.23, 7839.64, 19560.04, 14509.24, 17360.28, 14469.16, 12700.89, 18474.68, 13031.67, 15394.18]
}
    df = pd.DataFrame(data_dict)
    df.to_csv(csv_file, index=False)
    print(f" Sample CSV '{csv_file}' created successfully.")
else:
    print(f" Found existing dataset: {csv_file}")

# Read data
data = pd.read_csv(csv_file)   
print("\n First 5 rows of data:")
print(data.head())

# -----------------------------------
# 2 Data Storage (SQLite)
# -----------------------------------
print("\nData Storage\n")

# Connect to SQLite DB
conn = sqlite3.connect("hospital_db.sqlite")

# Store data in SQLite
data.to_sql("patient_bills", conn, if_exists="replace", index=False)
print("Data successfully stored in 'hospital_db.sqlite' database.")

# Verify by reading back
df = pd.read_sql("SELECT * FROM patient_bills", conn)
print("\n Retrieved data from database:")
print(df.head())

# -----------------------------------
# 3️ Machine Learning
# -----------------------------------
print("\nMachine Learning\n")

# Feature and target
X = df[["Room_Charges" , "Consultation_Hours" , "Num_Tests", "Days_Admitted" , "Age"]]
y = df["Total_Bill"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

model_filename = 'my_model.joblib'
print(f"\nSaving Model to {model_filename}")

joblib.dump(model , model_filename)
print("\nModel Saved Successfully")

print(f"Loading model from {model_filename}")
loaded_model = joblib.load(model_filename)
print("\nModel Loaded Successfully")

# Predict
predictions = loaded_model.predict(X_test)
# print(predictions)

# Evaluate model
mse = mean_squared_error(y_test, predictions)
print(f" Model trained successfully. Mean Squared Error: {mse:.2f}")

# Combine results for visualization
results_df = X_test.copy()
results_df["Actual Total Bill"] = y_test.values
results_df["Predicted Total Bill"] = predictions

print("\nPredictions\n")
print(results_df)

# -----------------------------------
# 4️ Visualization
# -----------------------------------
print("\nVisualization\n")

fig = px.scatter(
    results_df,
    x="Actual Total Bill",
    y="Predicted Total Bill",
    title="Actual vs Predicted Total Bill (Linear Regression)",
    size_max=10,
    color_discrete_sequence=["#2b8cbe"]
)

fig.update_layout(
    title_font=dict(size=20, color="darkblue"),
    xaxis_title="Actual Total Bill",
    yaxis_title="Predicted Total Bill",
    template="plotly_white"
)


print(fig.show())

print("\n End-to-End Data Pipeline Executed Successfully!")
