import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = sns.load_dataset('tips')
sns.set_style("whitegrid")
plt.figure(figsize=(7,5))
print(df.head())

# # 1. Bar Chart – Average tip by day
# sns.barplot(data=df, x="day", y="tip", palette="viridis" ,hue="day" )
# plt.title("Average Tip by Day")
# plt.annotate('Highest average tips on Sunday',
#              xy=(3, 3.5), xytext=(2, 4.1),
#              arrowprops=dict(facecolor='red', shrink=0.05 , width=1.5 ) , fontsize = 13, color = 'red')
# plt.show()

# # 2. Scatter Plot – Relationship between total bill and tip
# sns.scatterplot(data=df, x="total_bill", y="tip", hue="sex", style="time", s=70)
# plt.title("Tip vs Total Bill by Gender and Time")
# plt.show()

# # 3. Box Plot – Tip distribution by gender
# sns.boxplot(data=df, x="sex", y="tip", palette="pastel" , hue="sex")
# plt.title("Tip Distribution by Gender")
# plt.show()

print("\n Average Data Grouped by Lunch and Dinner")
df1 = df.groupby(['time'] , observed=True).mean(numeric_only=True)
print(df1)


print("\n Average Data Grouped by Male and Female")
df2 = df.groupby(['sex'] , observed=True).mean(numeric_only=True)
print(df2)


