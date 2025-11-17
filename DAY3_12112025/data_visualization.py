# #Step 1: Draw the bar chart
# import pandas as pd
# import plotly.express as px

# # -----------------------------
# # Step 1: Create sample dataset
# # -----------------------------

# data = {
#     "Category": ["Electronics", "Clothing", "Home Decor", "Books", "Beauty", "Sports"],
#     "Online_Sales": [145000, 89000, 67000, 32000, 45000, 59000],
#     "Offline_Sales": [59000, 45000, 32000, 67000, 89000, 145000],
#     "Orders": [1200, 1800, 950, 1300, 1100, 1000]
# }

# df = pd.DataFrame(data)

# sales_df_long = df.melt(
#     id_vars=['Category'],
#     value_vars=['Online_Sales', 'Offline_Sales'],
#     var_name='Sales_Type',
#     value_name='Sales'
# )


# fig = px.bar(
#     sales_df_long,
#     x="Category",
#     y="Sales",
#     color="Sales_Type", # Use 'Sales_Type' to create the grouped bars
#     text="Sales",
#     barmode="group",
#     title="E-Commerce Sales: Online vs. Offline by Category",
#     color_discrete_sequence=px.colors.qualitative.Safe
# )

# # Styling
# fig.update_traces(texttemplate='₹%{text:,.3s}', textposition='outside')
# fig.update_layout(
#     xaxis_title="Product Category",
#     yaxis_title="Sales (₹)",
#     title_font=dict(size=22, color="darkblue"),
#     template="plotly_white"
# )

# # -----------------------------
# # Step 3: Display Chart
# # -----------------------------
# fig.show()

import pandas as pd
import plotly.express as px

# -----------------------------
# Step 1: Create sample dataset
# -----------------------------
data = {
    "Category": ["Electronics", "Clothing", "Home Decor", "Books", "Beauty", "Sports"],
    "Total_Sales": [145000, 89000, 67000, 32000, 45000, 59000],
    "Orders": [1200, 1800, 950, 1300, 1100, 1000]
}

df = pd.DataFrame(data)

# -----------------------------
# Step 2: Bar Chart (Category-wise Sales)
# -----------------------------
fig = px.bar(
    df,
    x="Category",
    y="Total_Sales",
    text="Total_Sales",
    title="E-Commerce Sales by Product Category",
    color="Category",
    color_discrete_sequence=px.colors.qualitative.Safe
)

# Styling
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(
    xaxis_title="Product Category",
    yaxis_title="Total Sales (₹)",
    title_font=dict(size=22, color="darkblue"),
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    template="plotly_white"
)

# -----------------------------
# Step 3: Display Chart
# -----------------------------
fig.show()