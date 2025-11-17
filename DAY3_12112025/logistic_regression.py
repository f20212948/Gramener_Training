
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score , classification_report , confusion_matrix
import numpy as np
from sklearn.preprocessing import StandardScaler

# Step 1: Load dataset
data = pd.read_csv("./diabetes.csv")
print(" Data loaded successfully!")
print(data.head())

# Step 2: EDA and Model Training
cols_to_replace = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
data[cols_to_replace] = data[cols_to_replace].replace(0, np.nan)

# Impute missing values with the median of each column
for col in cols_to_replace:
    median_value = data[col].median()
    data[col].fillna(median_value,inplace=True)
    
    
X=data.drop('Outcome' , axis = 1)
y = data['Outcome']

X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.2,random_state=42)

scaler=StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_model = LogisticRegression()
log_model.fit(X_train_scaled , y_train)

y_pred = log_model.predict(X_test_scaled)



# Step 4: Evaluate

# Calculate Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}\n")

# Display Classification Report
print("--- Classification Report ---")
print(classification_report(y_test, y_pred))

# Display Confusion Matrix
print("--- Confusion Matrix ---")
print(confusion_matrix(y_test, y_pred))


# Step 5 : Visualize 
correlation_matrix = data.corr()

# Set up the Matplotlib figure
plt.figure(figsize=(10, 8))

# Create the Seaborn Heatmap
sns.heatmap(
    correlation_matrix,
    annot=True,          # Display the correlation values on the map
    cmap='coolwarm',     # Set the color scheme (cool colors for negative, warm for positive)
    fmt=".2f",           # Format the annotations to two decimal places
    linewidths=.5,       # Add lines between cells for clarity
    cbar_kws={'label': 'Correlation Coefficient'}
)

# Styling and Labels
plt.title('Correlation Heatmap of Diabetes Prediction Features', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout() # Adjust layout to prevent labels from being cut off
plt.show()