import pandas as pd

# Load the dataset
df = pd.read_csv("data/retail_sales_dataset.csv")

# Look at first 5 rows
print(df.head())

# Dataset structure
print(df.info())

# Summary stats
print(df.describe())

# Check missing values
print(df.isna().sum())
