
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load dataset
data = pd.read_csv("./diabetes.csv")
print(" Data loaded successfully!")
print(data.head())

# Step 2: Define simple rule-based function
def predict_diabetes(row):
    # Simple logic — not ML, just conditions
    if (
        row["Glucose"] > 130
        or row["BloodPressure"] > 85
        or row["BMI"] > 30
        or row["Age"] > 45
    ):
        return 1  # Diabetic
    else:
        return 0  # Non-diabetic

# Step 3: Apply logic to each row
data["Predicted_Outcome"] = data.apply(predict_diabetes, axis=1)

# Step 4: Evaluate
correct = (data["Predicted_Outcome"] == data["Outcome"]).sum()
accuracy = correct / len(data) * 100
print(f"\n Simple Rule-Based Accuracy: {accuracy:.2f}%")

# Step 5: Create bar chart for Actual vs Predicted
summary = (
    data[["Outcome", "Predicted_Outcome"]]
    .melt(var_name="Type", value_name="Value")
    .groupby(["Type", "Value"])
    .size()
    .reset_index(name="Count")
)

# # Step 6: Visualization
# fig = px.bar(
#     summary,
#     x="Value",
#     y="Count",
#     color="Type",
#     barmode="group",
#     text="Count",
#     color_discrete_sequence=["#1f77b4", "#ff7f0e"],
#     title="Actual vs Predicted Diabetes Cases (Rule-Based)"
# )

# fig.update_traces(texttemplate='%{text}', textposition='outside')
# fig.update_layout(
#     xaxis_title="Diabetes (0 = No, 1 = Yes)",
#     yaxis_title="Number of Patients",
#     title_font=dict(size=20, color="darkblue"),
#     template="plotly_white"
# )

# fig.show()

# Step 7: Visualization using seaborn
plt.figure(figsize=(8, 6))

# Use sns.barplot for a grouped bar chart
ax = sns.barplot(
    data=summary,
    x='Value',
    y='Count',
    hue='Type',  # Corresponds to 'color' in Plotly
    palette=['#ff6347', '#4682b4'] # Corresponds to color_discrete_sequence
)

# -----------------------------
# Styling (Matplotlib/Seaborn equivalent of Plotly's update_layout/update_traces)
# -----------------------------

# Set Title
ax.set_title(
    "Actual vs Predicted Diabetes Cases (Rule-Based) using Seaborn",
    fontsize=16,
    color="darkblue",
    pad=15 # Add padding to the title
)

# Set Axis Labels
ax.set_xlabel("Diabetes (0 = No, 1 = Yes)", fontsize=12)
ax.set_ylabel("Number of Patients", fontsize=12)

# Ensure x-ticks show the categorical values clearly
ax.set_xticklabels(['0', '1'])

# Add text annotations (equivalent of fig.update_traces(texttemplate='%{text}', textposition='outside'))
for container in ax.containers:
    ax.bar_label(container, fmt='%d', label_type='edge', padding=3)

# Remove the top and right spines for a cleaner look (similar to "plotly_white")
sns.despine(top=True, right=True)

# Display the plot
plt.show()


print("\n Visualization displayed successfully!")