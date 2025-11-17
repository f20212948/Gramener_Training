# ================================
# ETL Pipeline: Employee Data
# ================================

# ===== Import Libraries =====
import pandas as pd
import sqlite3

# ===== Extract Step =====
# Read employee data from CSV file
df = pd.read_csv("./employees.csv")

print("Original Data:")
print(df)

# ===== Transform Step =====
# 1. Increase salary of IT employees by 10%
df.loc[df['department'] == 'IT', 'salary'] *= 1.10

# 2. Standardize names to uppercase
df['name'] = df['name'].str.upper()

# 3. Add bonus = 5% of salary
df['bonus'] = df['salary'] * 0.05

print("\nTransformed Data:")
print(df)

# ===== Load Step =====
# Connect to SQLite (creates employees.db file if not exists)
conn = sqlite3.connect("employees.db")

# Write DataFrame to SQL table (replace if already exists)
df.to_sql("employees", conn, if_exists="replace", index=False)

print("\nData has been loaded into employees.db (table: employees)")

# ===== Verification Step =====
# Read back the data from database
result = pd.read_sql("SELECT * FROM employees", conn)
print(conn)
print("\nData from DB:")
print(result)

# Close connection
conn.close()
